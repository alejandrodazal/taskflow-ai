import subprocess
import json
from typing import Dict, Any, Optional
from taskflow.utils import get_logger
from taskflow.config import settings

class GeminiCLI:
    """Cliente simplificado para Gemini usando CLI."""
    
    def __init__(self):
        self.logger = get_logger(__name__)
        self.model = settings.gemini_model or "gemini-pro"
    
    def ask(self, prompt: str, context: Optional[str] = None) -> str:
        """Envía prompt a Gemini CLI y retorna respuesta."""
        try:
            # Construir prompt completo
            full_prompt = prompt
            if context:
                full_prompt = f"{prompt}\n\nContexto: {context}"
            
            # Ejecutar comando Gemini CLI
            cmd = [
                "gemini", 
                "generate", 
                "--model", self.model,
                "--prompt", full_prompt
            ]
            
            result = subprocess.run(
                cmd, 
                capture_output=True, 
                text=True, 
                encoding='utf-8'
            )
            
            if result.returncode == 0:
                return result.stdout.strip()
            else:
                self.logger.error(f"Error en Gemini CLI: {result.stderr}")
                return "Error al procesar la solicitud"
                
        except Exception as e:
            self.logger.error(f"Error ejecutando Gemini CLI: {e}")
            return "Error al conectar con Gemini"
    
    def interpret_command(self, user_input: str, tasks_context: str = "") -> Dict[str, Any]:
        """Interpreta comando del usuario usando Gemini CLI."""
        prompt = f"""
Interpreta este comando de gestión de tareas y responde SOLO con JSON válido:

Comando: "{user_input}"

Respuesta JSON debe tener:
{{
    "action": "create_task|complete_task|list_tasks|search_tasks|generate_kanban",
    "description": "descripción si aplica",
    "project": "proyecto si aplica",
    "priority": "low|normal|high",
    "task_id": "ID si aplica",
    "message": "respuesta al usuario"
}}
"""
        
        response = self.ask(prompt, tasks_context)
        
        try:
            # Extraer JSON de la respuesta
            import re
            json_match = re.search(r'\{.*\}', response, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
        except:
            pass
        
        # Fallback si no se puede parsear JSON
        return {
            "action": "unknown",
            "message": "No pude interpretar el comando"
        }