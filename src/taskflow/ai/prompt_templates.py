from typing import List, Dict, Any, Optional

class PromptTemplates:
    """Plantillas de prompts para diferentes funcionalidades."""
    
    def get_command_interpretation_prompt(self, user_input: str) -> str:
        """Prompt para interpretar comandos del usuario."""
        return f"""
Eres un asistente de gestión de tareas que interpreta comandos en lenguaje natural.
Debes convertir el siguiente comando del usuario en una acción estructurada.

Comando del usuario: "{user_input}"

Responde ÚNICAMENTE con un JSON válido que contenga:
{{
    "action": "create_task|complete_task|update_task|list_tasks|create_project|delete_task|search_tasks|generate_kanban|get_summary",
    "description": "descripción de la tarea (si aplica)",
    "project": "nombre del proyecto (si aplica)",
    "priority": "low|normal|high (si aplica)",
    "due_date": "fecha límite en formato natural (si aplica)",
    "task_id": "ID de la tarea (si aplica)",
    "tags": ["lista", "de", "etiquetas"] (si aplica),
    "query": "término de búsqueda (si aplica)",
    "message": "mensaje de respuesta al usuario"
}}

Ejemplos:
- "Crea una tarea para revisar el código" → {{"action": "create_task", "description": "revisar el código", "message": "Tarea creada para revisar el código"}}
- "Completa la tarea 5" → {{"action": "complete_task", "task_id": "5", "message": "Tarea 5 completada"}}
- "Muestra mis tareas pendientes" → {{"action": "list_tasks", "message": "Aquí están tus tareas pendientes"}}
- "Genera tablero kanban del proyecto web" → {{"action": "generate_kanban", "project": "web", "message": "Generando tablero Kanban del proyecto web"}}
"""
    
    def get_task_generation_prompt(self, project_description: str) -> str:
        """Prompt para generar lista de tareas de un proyecto."""
        return f"""
Genera una lista detallada de tareas para el siguiente proyecto:

"{project_description}"

Crea entre 5-10 tareas específicas y accionables. Cada tarea debe:
- Ser clara y específica
- Tener un verbo de acción
- Ser completable en un tiempo razonable
- Estar ordenada lógicamente

Formato de respuesta (una tarea por línea):
- Tarea 1: descripción específica
- Tarea 2: descripción específica
- etc.

Ejemplo para "Crear una aplicación web de tareas":
- Diseñar la arquitectura de la aplicación
- Crear mockups de la interfaz de usuario
- Configurar el entorno de desarrollo
- Implementar el backend con API REST
- Desarrollar la interfaz de usuario
- Integrar frontend con backend
- Escribir tests unitarios
- Realizar pruebas de integración
- Desplegar en servidor de producción
- Documentar el proyecto
"""
    
    def get_summary_prompt(self, tasks: List[Dict[str, Any]], project: Optional[str] = None) -> str:
        """Prompt para generar resumen de tareas para voz."""
        project_text = f" del proyecto {project}" if project else ""
        tasks_text = "\n".join([f"- {task.get('description', 'Sin descripción')} ({task.get('status', 'pending')})" for task in tasks])
        
        return f"""
Genera un resumen conciso y natural en español para síntesis de voz sobre las siguientes tareas{project_text}:

{tasks_text}

El resumen debe:
- Ser natural para escuchar (no leer)
- Mencionar el número total de tareas
- Destacar tareas importantes o urgentes
- Ser positivo y motivador
- No exceder 30 segundos de lectura

Ejemplo: "Tienes 5 tareas pendientes en tu proyecto web. Las más importantes son revisar el código y completar las pruebas. ¡Vas por buen camino!"
"""
    
    def get_github_issue_prompt(self, task: Dict[str, Any]) -> str:
        """Prompt para generar descripción de issue de GitHub."""
        return f"""
Convierte la siguiente tarea en una descripción detallada para un issue de GitHub:

Tarea: {task.get('description', '')}
Proyecto: {task.get('project', 'N/A')}
Prioridad: {task.get('priority', 'normal')}
Fecha límite: {task.get('due', 'N/A')}

Genera:
1. Un título claro y descriptivo
2. Una descripción detallada con:
   - Contexto del problema/tarea
   - Criterios de aceptación
   - Pasos sugeridos (si aplica)
   - Etiquetas recomendadas

Formato:
**Título:** [título del issue]

**Descripción:**
[descripción detallada]

**Criterios de aceptación:**
- [ ] Criterio 1
- [ ] Criterio 2

**Etiquetas:** enhancement, bug, documentation, etc.
"""