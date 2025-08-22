import click
from rich.console import Console
from rich.table import Table
from taskflow.taskwarrior import TaskManager
from taskflow.ai.gemini_cli import GeminiCLI
from taskflow.github import SyncManager
from taskflow.voice import TTSEngine
from taskflow.kanban import KanbanGenerator
from taskflow.utils import get_logger, format_task_for_display
from taskflow.config import settings

console = Console()
logger = get_logger(__name__)

@click.group()
@click.version_option(version="1.1.0")
def cli():
    """TaskFlow AI - Gestión inteligente de tareas con IA."""
    pass

@cli.command()
@click.argument('query', nargs=-1, required=True)
@click.option('--voice', '-v', is_flag=True, help='Respuesta por voz')
@click.option('--sync', '-s', is_flag=True, help='Sincronizar con GitHub')
def ask(query, voice, sync):
    """Comando principal: interpreta consultas en lenguaje natural."""
    try:
        user_input = ' '.join(query)
        console.print(f"[bold blue]🤖 Procesando:[/bold blue] {user_input}")
        
        # Inicializar componentes
        task_manager = TaskManager()
        gemini = GeminiCLI()
        
        # Obtener contexto actual
        current_tasks = task_manager.get_tasks()
        context = f"Tareas actuales: {len(current_tasks)} pendientes"
        
        # Interpretar comando
        response = gemini.interpret_command(user_input, context)
        
        # Ejecutar acción
        result = execute_action(response, task_manager)
        
        # Mostrar resultado
        console.print(f"[green]✅ {result}[/green]")
        
        # Síntesis de voz si se solicita
        if voice:
            tts = TTSEngine()
            tts.speak(result)
        
        # Sincronización con GitHub si se solicita
        if sync:
            sync_manager = SyncManager()
            sync_result = sync_manager.sync_all_pending_tasks()
            console.print(f"[blue]🔄 Sincronizado: {sync_result['synced']} tareas[/blue]")
            
    except Exception as e:
        logger.error(f"Error en comando ask: {e}")
        console.print(f"[red]❌ Error: {e}[/red]")

def execute_action(response: dict, task_manager: TaskManager) -> str:
    """Ejecuta la acción interpretada por la IA."""
    action = response.get('action', 'unknown')
    
    if action == 'create_task':
        task = task_manager.add_task(
            description=response.get('description', ''),
            project=response.get('project'),
            priority=response.get('priority'),
            due=response.get('due_date'),
            tags=response.get('tags')
        )
        return f"Tarea creada: {task.get('description', '')}"
    
    elif action == 'complete_task':
        task_id = response.get('task_id')
        if task_id:
            task_manager.complete_task(task_id)
            return f"Tarea {task_id} completada"
        return "ID de tarea requerido"
    
    elif action == 'list_tasks':
        tasks = task_manager.get_tasks(project=response.get('project'))
        if tasks:
            table = Table(title="Tareas Pendientes")
            table.add_column("ID", style="cyan")
            table.add_column("Descripción", style="white")
            table.add_column("Proyecto", style="green")
            table.add_column("Prioridad", style="yellow")
            
            for task in tasks[:10]:  # Mostrar máximo 10
                table.add_row(
                    str(task.get('id', '')),
                    task.get('description', ''),
                    task.get('project', ''),
                    task.get('priority', '')
                )
            
            console.print(table)
            return f"Mostrando {len(tasks)} tareas"
        return "No hay tareas pendientes"
    
    elif action == 'search_tasks':
        query = response.get('query', '')
        tasks = task_manager.search_tasks(query)
        return f"Encontradas {len(tasks)} tareas con '{query}'"
    
    elif action == 'generate_kanban':
        kanban = KanbanGenerator()
        project = response.get('project')
        filename = kanban.generate_board(project)
        return f"Tablero Kanban generado: {filename}"
    
    else:
        return response.get('message', 'Comando no reconocido')

if __name__ == '__main__':
    cli()