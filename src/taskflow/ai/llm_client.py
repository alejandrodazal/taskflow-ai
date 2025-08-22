import google.generativeai as genai
import openai
import json
import re
from typing import Dict, Any, Optional, List
from abc import ABC, abstractmethod
from taskflow.config import settings
from taskflow.utils import get_logger
from .prompt_templates import PromptTemplates

class LLMProvider(ABC):
    """Interfaz abstracta para proveedores de LLM."""
    
    @abstractmethod
    def generate_response(self, prompt: str, context: Dict[str, Any] = None) -> str:
        pass

class GeminiProvider(LLMProvider):
    """Proveedor para Google Gemini AI."""
    
    def __init__(self, api_key: str, model: str = "gemini-pro"):
        self.api_key = api_key
        self.model = model
        self.logger = get_logger(__name__)
        
        # Configurar Gemini
        genai.configure(api_key=api_key)
        self.client = genai.GenerativeModel(model)
        
    def generate_response(self, prompt: str, context: Dict[str, Any] = None) -> str:
        """Genera respuesta usando Gemini."""
        try:
            # Añadir contexto al prompt si existe
            if context:
                context_str = json.dumps(context, indent=2, ensure_ascii=False)
                full_prompt = f"{prompt}\n\nContexto actual:\n{context_str}"
            else:
                full_prompt = prompt
            
            response = self.client.generate_content(full_prompt)
            return response.text
            
        except Exception as e:
            self.logger.error(f"Error generando respuesta con Gemini: {e}")
            raise

class OpenAIProvider(LLMProvider):
    """Proveedor para OpenAI (fallback)."""
    
    def __init__(self, api_key: str, model: str = "gpt-3.5-turbo"):
        self.client = openai.OpenAI(api_key=api_key)
        self.model = model
        self.logger = get_logger(__name__)
    
    def generate_response(self, prompt: str, context: Dict[str, Any] = None) -> str:
        """Genera respuesta usando OpenAI."""
        try:
            messages = [{"role": "user", "content": prompt}]
            
            if context:
                context_str = json.dumps(context, indent=2, ensure_ascii=False)
                messages.insert(0, {
                    "role": "system", 
                    "content": f"Contexto actual: {context_str}"
                })
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.7
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            self.logger.error(f"Error generando respuesta con OpenAI: {e}")
            raise

class LLMClient:
    """Cliente principal para interactuar con LLMs."""
    
    def __init__(self):
        self.settings = settings
        self.logger = get_logger(__name__)
        self.templates = PromptTemplates()
        self.provider = self._initialize_provider()
    
    def _initialize_provider(self) -> LLMProvider:
        """Inicializa el proveedor de LLM según la configuración."""
        if self.settings.llm_provider == "gemini":
            return GeminiProvider(
                api_key=self.settings.gemini_api_key,
                model=self.settings.gemini_model
            )
        elif self.settings.llm_provider == "openai":
            if not self.settings.openai_api_key:
                raise ValueError("OpenAI API key is required for OpenAI provider")
            return OpenAIProvider(
                api_key=self.settings.openai_api_key,
                model=self.settings.openai_model
            )
        else:
            raise ValueError(f"Unsupported LLM provider: {self.settings.llm_provider}")
    
    def interpret_command(self, user_input: str, current_tasks: List[Dict] = None) -> Dict[str, Any]:
        """Interpreta comando en lenguaje natural y retorna acción estructurada."""
        try:
            context = {
                "current_tasks": current_tasks or [],
                "available_projects": self._get_available_projects()
            }
            
            prompt = self.templates.get_command_interpretation_prompt(user_input)
            response = self.provider.generate_response(prompt, context)
            
            # Parsear respuesta JSON
            return self._parse_command_response(response)
            
        except Exception as e:
            self.logger.error(f"Error interpretando comando: {e}")
            return {
                "action": "error",
                "message": f"No pude interpretar el comando: {str(e)}"
            }
    
    def generate_task_list(self, project_description: str) -> List[Dict[str, Any]]:
        """Genera lista de tareas basada en descripción del proyecto."""
        try:
            prompt = self.templates.get_task_generation_prompt(project_description)
            response = self.provider.generate_response(prompt)
            
            return self._parse_task_list_response(response)
            
        except Exception as e:
            self.logger.error(f"Error generando lista de tareas: {e}")
            return []
    
    def generate_summary(self, tasks: List[Dict[str, Any]], project: str = None) -> str:
        """Genera resumen de tareas para síntesis de voz."""
        try:
            prompt = self.templates.get_summary_prompt(tasks, project)
            return self.provider.generate_response(prompt)
            
        except Exception as e:
            self.logger.error(f"Error generando resumen: {e}")
            return "No pude generar el resumen de tareas."
    
    def _parse_command_response(self, response: str) -> Dict[str, Any]:
        """Parsea la respuesta del LLM para extraer comando estructurado."""
        try:
            # Buscar JSON en la respuesta
            json_match = re.search(r'\{.*\}', response, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
            
            # Si no hay JSON, intentar parsear manualmente
            return self._manual_parse_command(response)
            
        except json.JSONDecodeError:
            return self._manual_parse_command(response)
    
    def _manual_parse_command(self, response: str) -> Dict[str, Any]:
        """Parseo manual cuando el JSON falla."""
        response_lower = response.lower()
        
        if any(word in response_lower for word in ['crear', 'añadir', 'nueva tarea']):
            return {
                "action": "create_task",
                "description": response,
                "project": None,
                "priority": "normal"
            }
        elif any(word in response_lower for word in ['completar', 'terminar', 'finalizar']):
            return {
                "action": "complete_task",
                "task_id": None
            }
        elif any(word in response_lower for word in ['listar', 'mostrar', 'ver tareas']):
            return {
                "action": "list_tasks",
                "project": None
            }
        else:
            return {
                "action": "unknown",
                "message": "No pude interpretar el comando"
            }
    
    def _parse_task_list_response(self, response: str) -> List[Dict[str, Any]]:
        """Parsea lista de tareas generada por el LLM."""
        tasks = []
        lines = response.split('\n')
        
        for line in lines:
            line = line.strip()
            if line and (line.startswith('-') or line.startswith('*') or line[0].isdigit()):
                # Limpiar formato de lista
                task_desc = re.sub(r'^[-*\d\.\)\s]+', '', line).strip()
                if task_desc:
                    tasks.append({
                        "description": task_desc,
                        "priority": "normal",
                        "status": "pending"
                    })
        
        return tasks
    
    def _get_available_projects(self) -> List[str]:
        """Obtiene proyectos disponibles (placeholder)."""
        # Esto se implementará cuando se integre con TaskManager
        return []