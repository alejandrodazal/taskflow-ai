import click
from rich.console import Console
from taskflow.taskwarrior import TaskManager
from taskflow.github import SyncManager
from taskflow.kanban import KanbanGenerator
from .main import cli

console = Console()

@cli.command()
@click.option('--project', '-p', help='Filtrar por proyecto')
def list(project):
    """Lista todas las tareas."""
    task_manager = TaskManager()
    tasks = task_manager.get_tasks(project=project)
    
    if not tasks:
        console.print("[yellow]No hay tareas pendientes[/yellow]")
        return
    
    for task in tasks:
        formatted = format_task_for_display(task)
        console.print(formatted)

@cli.command()
@click.argument('description')
@click.option('--project', '-p', help='Proyecto')
@click.option('--priority', '-pr', type=click.Choice(['low', 'normal', 'high']), default='normal')
@click.option('--due', '-d', help='Fecha límite')
def add(description, project, priority, due):
    """Añade una nueva tarea."""
    task_manager = TaskManager()
    task = task_manager.add_task(
        description=description,
        project=project,
        priority=priority,
        due=due
    )
    console.print(f"[green]✅ Tarea creada: {description}[/green]")

@cli.command()
@click.argument('task_id')
def done(task_id):
    """Marca una tarea como completada."""
    task_manager = TaskManager()
    task_manager.complete_task(task_id)
    console.print(f"[green]✅ Tarea {task_id} completada[/green]")

@cli.command()
def sync():
    """Sincroniza tareas con GitHub."""
    sync_manager = SyncManager()
    result = sync_manager.sync_all_pending_tasks()
    console.print(f"[blue]🔄 Sincronizadas {result['synced']} tareas[/blue]")

@cli.command()
@click.option('--project', '-p', help='Proyecto específico')
def kanban(project):
    """Genera tablero Kanban."""
    generator = KanbanGenerator()
    filename = generator.generate_board(project)
    console.print(f"[green]📊 Tablero generado: {filename}[/green]")