from taskw import TaskWarrior
from typing import List, Dict, Any, Optional
from datetime import datetime
from taskflow.utils import get_logger, parse_natural_date
from taskflow.config import settings

class TaskManager:
    """Gestor de tareas usando Taskwarrior."""
    
    def __init__(self):
        self.tw = TaskWarrior()
        self.logger = get_logger(__name__)
    
    def create_project(self, name: str, description: str = "") -> str:
        """Crea un nuevo proyecto."""
        try:
            # En Taskwarrior, los proyectos se crean implícitamente al asignar tareas
            self.logger.info(f"Proyecto '{name}' creado")
            return name
        except Exception as e:
            self.logger.error(f"Error creando proyecto: {e}")
            raise
    
    def add_task(self, description: str, project: str = None, 
                 priority: str = None, due: str = None, tags: List[str] = None) -> Dict[str, Any]:
        """Añade una nueva tarea."""
        try:
            task_data = {'description': description}
            
            if project:
                task_data['project'] = project
            
            if priority:
                task_data['priority'] = priority
            
            if due:
                parsed_due = parse_natural_date(due)
                if parsed_due:
                    task_data['due'] = parsed_due.strftime('%Y-%m-%d')
            
            if tags:
                task_data['tags'] = tags
            
            task = self.tw.task_add(**task_data)
            self.logger.info(f"Tarea creada: {description}")
            return task
        except Exception as e:
            self.logger.error(f"Error añadiendo tarea: {e}")
            raise
    
    def update_task(self, task_id: str, **kwargs) -> Dict[str, Any]:
        """Actualiza una tarea existente."""
        try:
            # Filtrar valores None
            update_data = {k: v for k, v in kwargs.items() if v is not None}
            
            if 'due' in update_data:
                parsed_due = parse_natural_date(str(update_data['due']))
                if parsed_due:
                    update_data['due'] = parsed_due.strftime('%Y-%m-%d')
            
            task = self.tw.task_update(task_id, **update_data)
            self.logger.info(f"Tarea {task_id} actualizada")
            return task
        except Exception as e:
            self.logger.error(f"Error actualizando tarea: {e}")
            raise
    
    def complete_task(self, task_id: str) -> Dict[str, Any]:
        """Marca una tarea como completada."""
        try:
            task = self.tw.task_done(task_id)
            self.logger.info(f"Tarea {task_id} completada")
            return task
        except Exception as e:
            self.logger.error(f"Error completando tarea: {e}")
            raise
    
    def delete_task(self, task_id: str) -> Dict[str, Any]:
        """Elimina una tarea."""
        try:
            task = self.tw.task_delete(task_id)
            self.logger.info(f"Tarea {task_id} eliminada")
            return task
        except Exception as e:
            self.logger.error(f"Error eliminando tarea: {e}")
            raise
    
    def get_tasks(self, project: str = None, status: str = "pending") -> List[Dict[str, Any]]:
        """Obtiene lista de tareas."""
        try:
            filters = {'status': status}
            if project:
                filters['project'] = project
            
            tasks = self.tw.load_tasks()
            filtered_tasks = []
            
            for task in tasks['pending'] if status == 'pending' else tasks['completed']:
                if project and task.get('project') != project:
                    continue
                filtered_tasks.append(task)
            
            return filtered_tasks
        except Exception as e:
            self.logger.error(f"Error obteniendo tareas: {e}")
            raise
    
    def get_projects(self) -> List[str]:
        """Obtiene lista de proyectos."""
        try:
            tasks = self.tw.load_tasks()
            projects = set()
            
            for task in tasks['pending'] + tasks['completed']:
                if 'project' in task:
                    projects.add(task['project'])
            
            return sorted(list(projects))
        except Exception as e:
            self.logger.error(f"Error obteniendo proyectos: {e}")
            raise
    
    def search_tasks(self, query: str) -> List[Dict[str, Any]]:
        """Busca tareas por descripción."""
        try:
            all_tasks = self.get_tasks()
            matching_tasks = []
            
            query_lower = query.lower()
            for task in all_tasks:
                if query_lower in task.get('description', '').lower():
                    matching_tasks.append(task)
            
            return matching_tasks
        except Exception as e:
            self.logger.error(f"Error buscando tareas: {e}")
            raise
    
    def get_task_by_id(self, task_id: str) -> Optional[Dict[str, Any]]:
        """Obtiene una tarea por su ID."""
        try:
            tasks = self.tw.load_tasks()
            
            for task in tasks['pending'] + tasks['completed']:
                if str(task.get('id')) == str(task_id) or str(task.get('uuid')) == str(task_id):
                    return task
            
            return None
        except Exception as e:
            self.logger.error(f"Error obteniendo tarea por ID: {e}")
            raise