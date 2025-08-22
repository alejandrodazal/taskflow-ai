from typing import Dict, Any, Optional, List
from taskflow.taskwarrior import TaskManager
from .github_client import GitHubClient
from taskflow.ai import LLMClient
from taskflow.utils import get_logger, save_json, load_json
from pathlib import Path
import json

class SyncManager:
    """Gestor de sincronización entre Taskwarrior y GitHub."""
    
    def __init__(self):
        self.github_client = GitHubClient()
        self.task_manager = TaskManager()
        self.llm_client = LLMClient()
        self.logger = get_logger(__name__)
        
        # Archivo para mapear tareas con issues
        self.mapping_file = Path("task_github_mapping.json")
        self.task_issue_map = self._load_mapping()
    
    def _load_mapping(self) -> Dict[str, int]:
        """Carga el mapeo de tareas a issues desde archivo."""
        return load_json(self.mapping_file)
    
    def _save_mapping(self) -> None:
        """Guarda el mapeo de tareas a issues."""
        save_json(self.task_issue_map, self.mapping_file)
    
    def sync_task_to_github(self, task: Dict[str, Any]) -> Optional[int]:
        """Sincroniza una tarea de Taskwarrior a GitHub."""
        try:
            task_uuid = task.get('uuid')
            if not task_uuid:
                self.logger.error("Tarea sin UUID, no se puede sincronizar")
                return None
            
            # Verificar si ya existe un issue para esta tarea
            if task_uuid in self.task_issue_map:
                issue_number = self.task_issue_map[task_uuid]
                return self._update_existing_issue(task, issue_number)
            else:
                return self._create_new_issue(task)
                
        except Exception as e:
            self.logger.error(f"Error sincronizando tarea: {e}")
            return None
    
    def _create_new_issue(self, task: Dict[str, Any]) -> Optional[int]:
        """Crea un nuevo issue para la tarea."""
        try:
            # Generar contenido del issue usando IA
            issue_content = self.llm_client.provider.generate_response(
                self.llm_client.templates.get_github_issue_prompt(task)
            )
            
            # Parsear título y descripción
            title, body = self._parse_issue_content(issue_content, task)
            
            # Determinar etiquetas
            labels = self._get_task_labels(task)
            
            # Crear issue
            issue_data = self.github_client.create_issue(
                title=title,
                body=body,
                labels=labels
            )
            
            # Guardar mapeo
            task_uuid = task.get('uuid')
            issue_number = issue_data['number']
            self.task_issue_map[task_uuid] = issue_number
            self._save_mapping()
            
            self.logger.info(f"Issue #{issue_number} creado para tarea {task_uuid}")
            return issue_number
            
        except Exception as e:
            self.logger.error(f"Error creando issue: {e}")
            return None
    
    def _update_existing_issue(self, task: Dict[str, Any], issue_number: int) -> int:
        """Actualiza un issue existente."""
        try:
            # Determinar si necesita actualización
            task_status = task.get('status', 'pending')
            
            if task_status == 'completed':
                # Cerrar issue
                self.github_client.close_issue(
                    issue_number,
                    comment="✅ Tarea completada en TaskWarrior"
                )
                self.logger.info(f"Issue #{issue_number} cerrado (tarea completada)")
            elif task_status == 'deleted':
                # Cerrar issue con comentario diferente
                self.github_client.close_issue(
                    issue_number,
                    comment="❌ Tarea eliminada en TaskWarrior"
                )
                self.logger.info(f"Issue #{issue_number} cerrado (tarea eliminada)")
            
            return issue_number
            
        except Exception as e:
            self.logger.error(f"Error actualizando issue: {e}")
            return issue_number
    
    def _parse_issue_content(self, content: str, task: Dict[str, Any]) -> tuple:
        """Parsea el contenido generado por IA para extraer título y descripción."""
        lines = content.split('\n')
        title = task.get('description', 'Nueva tarea')
        body = content
        
        # Buscar título en el contenido
        for line in lines:
            if line.startswith('**Título:**'):
                title = line.replace('**Título:**', '').strip()
                break
            elif line.startswith('Título:'):
                title = line.replace('Título:', '').strip()
                break
        
        # Limpiar título de caracteres especiales
        title = title.replace('[', '').replace(']', '').strip()
        
        return title, body
    
    def _get_task_labels(self, task: Dict[str, Any]) -> List[str]:
        """Determina las etiquetas para el issue basado en la tarea."""
        labels = ['taskwarrior']
        
        # Etiqueta por prioridad
        priority = task.get('priority', '')
        if priority == 'H':
            labels.append('high-priority')
        elif priority == 'M':
            labels.append('medium-priority')
        elif priority == 'L':
            labels.append('low-priority')
        
        # Etiqueta por proyecto
        project = task.get('project', '')
        if project:
            labels.append(f'project-{project.lower()}')
        
        # Etiquetas por tags de la tarea
        task_tags = task.get('tags', [])
        for tag in task_tags:
            labels.append(f'tag-{tag.lower()}')
        
        return labels
    
    def sync_all_pending_tasks(self) -> Dict[str, Any]:
        """Sincroniza todas las tareas pendientes."""
        try:
            pending_tasks = self.task_manager.get_tasks(status="pending")
            
            results = {
                "synced": 0,
                "errors": 0,
                "issues_created": [],
                "issues_updated": []
            }
            
            for task in pending_tasks:
                issue_number = self.sync_task_to_github(task)
                if issue_number:
                    task_uuid = task.get('uuid')
                    if task_uuid not in self.task_issue_map:
                        results["issues_created"].append(issue_number)
                    else:
                        results["issues_updated"].append(issue_number)
                    results["synced"] += 1
                else:
                    results["errors"] += 1
            
            self.logger.info(f"Sincronización completada: {results['synced']} tareas")
            return results
            
        except Exception as e:
            self.logger.error(f"Error en sincronización masiva: {e}")
            return {"synced": 0, "errors": 1, "issues_created": [], "issues_updated": []}
    
    def get_sync_status(self) -> Dict[str, Any]:
        """Obtiene el estado de sincronización."""
        try:
            total_tasks = len(self.task_manager.get_tasks())
            synced_tasks = len(self.task_issue_map)
            
            return {
                "total_tasks": total_tasks,
                "synced_tasks": synced_tasks,
                "sync_percentage": (synced_tasks / total_tasks * 100) if total_tasks > 0 else 0,
                "mapping_file": str(self.mapping_file),
                "repo_info": self.github_client.get_repo_info()
            }
            
        except Exception as e:
            self.logger.error(f"Error obteniendo estado de sync: {e}")
            return {}