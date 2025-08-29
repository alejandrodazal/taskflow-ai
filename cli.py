import click
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from kanban_app.database import init_db, get_session
from kanban_app.models import Task, Project, Assignee, TaskStatus, Priority

console = Console()

@click.group()
@click.version_option(version="1.0.0")
def cli():
    """TaskFlow Kanban CLI - Gestión de tareas con tablero Kanban"""
    pass

@cli.command()
def init():
    """Inicializar la base de datos"""
    try:
        init_db()
        console.print("[green]+ Base de datos inicializada correctamente[/green]")
    except Exception as e:
        console.print(f"[red]x Error al inicializar la base de datos: {e}[/red]")

@cli.command()
@click.argument('name')
@click.option('--description', '-d', help='Descripción del proyecto')
def create_project(name, description):
    """Crear un nuevo proyecto"""
    try:
        db = get_session()
        
        # Verificar si el proyecto ya existe
        existing = db.query(Project).filter(Project.name == name).first()
        if existing:
            console.print(f"[yellow]* El proyecto '{name}' ya existe[/yellow]")
            return
        
        project = Project(name=name, description=description)
        db.add(project)
        db.commit()
        db.refresh(project)
        
        console.print(f"[green]+ Proyecto '{name}' creado con ID: {project.id}[/green]")
        db.close()
    except Exception as e:
        console.print(f"[red]✗ Error al crear el proyecto: {e}[/red]")

@cli.command()
@click.argument('name')
@click.option('--email', '-e', help='Email del responsable')
def create_assignee(name, email):
    """Crear un nuevo responsable"""
    try:
        db = get_session()
        
        # Verificar si el responsable ya existe
        existing = db.query(Assignee).filter(Assignee.name == name).first()
        if existing:
            console.print(f"[yellow]* El responsable '{name}' ya existe[/yellow]")
            return
        
        assignee = Assignee(name=name, email=email)
        db.add(assignee)
        db.commit()
        db.refresh(assignee)
        
        console.print(f"[green]+ Responsable '{name}' creado con ID: {assignee.id}[/green]")
        db.close()
    except Exception as e:
        console.print(f"[red]✗ Error al crear el responsable: {e}[/red]")

@cli.command()
@click.argument('title')
@click.option('--project', '-p', help='Nombre del proyecto')
@click.option('--assignee', '-a', help='Nombre del responsable')
@click.option('--priority', '-P', type=click.Choice(['low', 'medium', 'high']), default='medium', help='Prioridad')
@click.option('--description', '-d', help='Descripción de la tarea')
def create_task(title, project, assignee, priority, description):
    """Crear una nueva tarea"""
    try:
        db = get_session()
        
        # Buscar proyecto si se especifica
        project_id = None
        if project:
            proj = db.query(Project).filter(Project.name == project).first()
            if not proj:
                console.print(f"[yellow]* Creando proyecto '{project}'...[/yellow]")
                proj = Project(name=project)
                db.add(proj)
                db.commit()
                db.refresh(proj)
            project_id = proj.id
        
        # Buscar responsable si se especifica
        assignee_id = None
        if assignee:
            assign = db.query(Assignee).filter(Assignee.name == assignee).first()
            if not assign:
                console.print(f"[yellow]* Creando responsable '{assignee}'...[/yellow]")
                assign = Assignee(name=assignee)
                db.add(assign)
                db.commit()
                db.refresh(assign)
            assignee_id = assign.id
        
        # Crear tarea
        task = Task(
            title=title,
            description=description,
            project_id=project_id,
            assignee_id=assignee_id,
            priority=Priority(priority)
        )
        
        db.add(task)
        db.commit()
        db.refresh(task)
        
        console.print(f"[green]+ Tarea '{title}' creada con ID: {task.id}[/green]")
        db.close()
    except Exception as e:
        console.print(f"[red]✗ Error al crear la tarea: {e}[/red]")

@cli.command()
@click.argument('task_id', type=int)
def complete_task(task_id):
    """Marcar una tarea como completada"""
    try:
        db = get_session()
        
        task = db.query(Task).filter(Task.id == task_id).first()
        if not task:
            console.print(f"[red]x Tarea con ID {task_id} no encontrada[/red]")
            return
        
        task.status = TaskStatus.COMPLETED
        task.updated_at = Task.__table__.c.updated_at.default.arg
        db.commit()
        
        console.print(f"[green]+ Tarea '{task.title}' marcada como completada[/green]")
        db.close()
    except Exception as e:
        console.print(f"[red]✗ Error al completar la tarea: {e}[/red]")

@cli.command()
def list_projects():
    """Listar todos los proyectos"""
    try:
        db = get_session()
        projects = db.query(Project).all()
        
        if not projects:
            console.print("[yellow]No hay proyectos registrados[/yellow]")
            return
        
        table = Table(title="Proyectos")
        table.add_column("ID", style="cyan")
        table.add_column("Nombre", style="green")
        table.add_column("Descripción", style="white")
        table.add_column("Tareas", style="yellow")
        
        for project in projects:
            # Contar tareas del proyecto
            task_count = db.query(Task).filter(Task.project_id == project.id).count()
            table.add_row(
                str(project.id),
                project.name,
                project.description or "",
                str(task_count)
            )
        
        console.print(table)
        db.close()
    except Exception as e:
        console.print(f"[red]✗ Error al listar proyectos: {e}[/red]")

@cli.command()
def list_assignees():
    """Listar todos los responsables"""
    try:
        db = get_session()
        assignees = db.query(Assignee).all()
        
        if not assignees:
            console.print("[yellow]No hay responsables registrados[/yellow]")
            return
        
        table = Table(title="Responsables")
        table.add_column("ID", style="cyan")
        table.add_column("Nombre", style="green")
        table.add_column("Email", style="white")
        table.add_column("Tareas", style="yellow")
        
        for assignee in assignees:
            # Contar tareas del responsable
            task_count = db.query(Task).filter(Task.assignee_id == assignee.id).count()
            table.add_row(
                str(assignee.id),
                assignee.name,
                assignee.email or "",
                str(task_count)
            )
        
        console.print(table)
        db.close()
    except Exception as e:
        console.print(f"[red]✗ Error al listar responsables: {e}[/red]")

@cli.command()
@click.option('--project', '-p', help='Filtrar por proyecto')
@click.option('--assignee', '-a', help='Filtrar por responsable')
@click.option('--status', '-s', type=click.Choice(['pending', 'inprogress', 'completed']), help='Filtrar por estado')
def list_tasks(project, assignee, status):
    """Listar todas las tareas"""
    try:
        db = get_session()
        query = db.query(Task)
        
        # Aplicar filtros
        if project:
            proj = db.query(Project).filter(Project.name == project).first()
            if proj:
                query = query.filter(Task.project_id == proj.id)
            else:
                console.print(f"[yellow]* Proyecto '{project}' no encontrado[/yellow]")
                return
        
        if assignee:
            assign = db.query(Assignee).filter(Assignee.name == assignee).first()
            if assign:
                query = query.filter(Task.assignee_id == assign.id)
            else:
                console.print(f"[yellow]* Responsable '{assignee}' no encontrado[/yellow]")
                return
        
        if status:
            query = query.filter(Task.status == TaskStatus(status))
        
        tasks = query.all()
        
        if not tasks:
            console.print("[yellow]No hay tareas que coincidan con los criterios[/yellow]")
            return
        
        table = Table(title="Tareas")
        table.add_column("ID", style="cyan")
        table.add_column("Título", style="green")
        table.add_column("Proyecto", style="blue")
        table.add_column("Responsable", style="magenta")
        table.add_column("Prioridad", style="yellow")
        table.add_column("Estado", style="white")
        
        for task in tasks:
            table.add_row(
                str(task.id),
                task.title,
                task.project_name or "Sin proyecto",
                task.assignee_name or "Sin asignar",
                task.priority.value if task.priority else "media",
                task.status.value if task.status else "pendiente"
            )
        
        console.print(table)
        db.close()
    except Exception as e:
        console.print(f"[red]✗ Error al listar tareas: {e}[/red]")

@cli.command()
def kanban():
    """Mostrar tablero Kanban en consola"""
    try:
        db = get_session()
        tasks = db.query(Task).all()
        
        if not tasks:
            console.print("[yellow]No hay tareas para mostrar[/yellow]")
            return
        
        # Organizar tareas por estado
        pending = [t for t in tasks if t.status == TaskStatus.PENDING]
        inprogress = [t for t in tasks if t.status == TaskStatus.IN_PROGRESS]
        completed = [t for t in tasks if t.status == TaskStatus.COMPLETED]
        
        # Crear paneles para cada columna
        pending_panel = Panel("\n".join([f"[cyan]{t.id}[/cyan] {t.title}" for t in pending]) or "[i]No hay tareas[/i]", 
                             title="Pendientes", style="red")
        inprogress_panel = Panel("\n".join([f"[cyan]{t.id}[/cyan] {t.title}" for t in inprogress]) or "[i]No hay tareas[/i]", 
                               title="En Progreso", style="blue")
        completed_panel = Panel("\n".join([f"[cyan]{t.id}[/cyan] {t.title}" for t in completed]) or "[i]No hay tareas[/i]", 
                              title="Completadas", style="green")
        
        # Mostrar tablero
        console.print("Tablero Kanban")
        console.print(pending_panel)
        console.print(inprogress_panel)
        console.print(completed_panel)
        
        db.close()
    except Exception as e:
        console.print(f"[red]✗ Error al mostrar el tablero Kanban: {e}[/red]")

if __name__ == '__main__':
    cli()