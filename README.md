# TaskFlow Kanban App

Una aplicación de gestión de tareas con tablero Kanban, diseñada para equipos que necesitan una herramienta visual e intuitiva para organizar su trabajo.

## Características

- **Tablero Kanban visual** con columnas para tareas pendientes, en progreso y completadas
- **Gestión de proyectos** y responsables
- **Interfaz web interactiva** con funcionalidad de arrastrar y soltar
- **Interfaz de línea de comandos (CLI)** para operaciones desde la terminal
- **Base de datos SQLite** para almacenamiento local
- **Prioridades de tareas** (baja, media, alta)
- **Filtros por proyecto y responsable**
- **Estadísticas en tiempo real** del progreso del trabajo

## Requisitos

- Python 3.8 o superior
- pip (gestor de paquetes de Python)

## Instalación

1. Clonar el repositorio o descargar los archivos
2. Instalar las dependencias:
   ```bash
   pip install -r kanban_app/requirements.txt
   ```

## Uso

### Inicializar la base de datos
```bash
python -m kanban_app.run init
```

### Interfaz web
Para iniciar el servidor web:
```bash
python -m kanban_app.run web
```
Luego abre tu navegador en `http://127.0.0.1:5002`

### Interfaz de línea de comandos
Para usar la CLI:
```bash
python -m kanban_app.run [comando]
```

#### Comandos disponibles:
- `init` - Inicializar la base de datos
- `create-project <nombre>` - Crear un nuevo proyecto
- `create-assignee <nombre>` - Crear un nuevo responsable
- `create-task <título>` - Crear una nueva tarea
- `complete-task <id>` - Marcar una tarea como completada
- `list-projects` - Listar todos los proyectos
- `list-assignees` - Listar todos los responsables
- `list-tasks` - Listar todas las tareas
- `kanban` - Mostrar tablero Kanban en consola

### Ejemplos de uso

#### Crear un proyecto y responsable:
```bash
python -m kanban_app.run create-project "Desarrollo Web" --description "Proyecto de desarrollo web"
python -m kanban_app.run create-assignee "Juan Pérez" --email "juan@example.com"
```

#### Crear tareas:
```bash
python -m kanban_app.run create-task "Diseñar interfaz" --project "Desarrollo Web" --assignee "Juan Pérez" --priority high
python -m kanban_app.run create-task "Implementar backend" --project "Desarrollo Web" --priority medium
```

#### Ver el tablero Kanban en consola:
```bash
python -m kanban_app.run kanban
```

## Estructura de la base de datos

La aplicación utiliza SQLite para almacenar la información en un archivo local `kanban.db` con las siguientes tablas:

- `projects` - Proyectos
- `assignees` - Responsables
- `tasks` - Tareas

## Funcionalidades web

La interfaz web incluye:

1. **Tablero Kanban interactivo** con arrastrar y soltar
2. **Formularios modales** para crear y editar tareas
3. **Estadísticas en tiempo real** del progreso
4. **Listado de proyectos y responsables**
5. **Filtros y búsqueda**

## Futuras mejoras

- Integración con reconocimiento de voz
- Notificaciones y recordatorios
- Exportación de datos
- Autenticación de usuarios
- Compartir tableros entre equipos

## Licencia

Este proyecto está bajo la licencia MIT.