# TaskFlow Kanban App - Especificación Técnica del Proyecto

## 1. Resumen Ejecutivo

TaskFlow Kanban App es una herramienta de gestión de proyectos para equipos, basada en un tablero Kanban visual. Permite la organización de tareas mediante una interfaz web interactiva y una interfaz de línea de comandos, con almacenamiento local en base de datos SQLite.

## 2. Arquitectura del Sistema

### 2.1 Arquitectura General
El sistema se compone de un backend en Python que contiene toda la lógica de negocio (gestión de tareas, proyectos y responsables) y dos interfaces de usuario:
1.  Una CLI tradicional para comandos directos.
2.  Una interfaz web para la gestión visual de tareas mediante tablero Kanban.

### 2.2 Arquitectura Web
- **Backend:** Un servidor web ligero (Flask) que expone una API RESTful.
- **Frontend:** Una página HTML única (Single Page Application) con JavaScript que permite la interacción visual con el tablero Kanban.
- **Comunicación:** El frontend envía solicitudes a la API del backend y muestra los resultados recibidos.

### 2.3 Arquitectura de Base de Datos
- **Motor:** SQLite para almacenamiento local.
- **Modelos:** Tres entidades principales (Projects, Assignees, Tasks) con relaciones adecuadas.
- **Persistencia:** Datos almacenados en archivo local `kanban.db`.

## 3. Modelo de Datos y Módulos

### 3.1 Entidades
- **Project:** Representa un proyecto con nombre y descripción.
- **Assignee:** Representa un responsable con nombre y email.
- **Task:** Representa una tarea con título, descripción, prioridad, estado y relaciones con Project y Assignee.

### 3.2 Módulos
- **Models:** Definición de entidades de datos.
- **Database:** Configuración y conexión a la base de datos.
- **Web:** Servidor Flask y rutas API.
- **CLI:** Interfaz de línea de comandos con comandos para gestión de tareas.

## 4. Dependencias Clave

```
Flask>=2.0.0
Flask-SQLAlchemy>=3.0.0
Flask-Migrate>=4.0.0
rich>=13.0.0
```

## 5. Casos de Uso y Comandos

### 5.1 Comandos CLI
```bash
# Inicializar base de datos
python -m kanban_app.run init

# Crear proyecto
python -m kanban_app.run create-project "Nombre" --description "Descripción"

# Crear responsable
python -m kanban_app.run create-assignee "Nombre" --email "email@example.com"

# Crear tarea
python -m kanban_app.run create-task "Título" --project "Proyecto" --assignee "Responsable" --priority high

# Completar tarea
python -m kanban_app.run complete-task ID

# Listar proyectos/responsables/tareas
python -m kanban_app.run list-projects
python -m kanban_app.run list-assignees
python -m kanban_app.run list-tasks

# Mostrar tablero Kanban en consola
python -m kanban_app.run kanban
```

### 5.2 Uso de la Interfaz Web
1. Ejecutar `python -m kanban_app.run web`.
2. Abrir navegador en `http://127.0.0.1:5002`.
3. Crear, editar, mover y filtrar tareas visualmente.

## 6. Roadmap de Desarrollo

### Fase 1: Base Funcional (Completada)
- [x] Implementar modelo de datos con SQLite.
- [x] Crear API RESTful para gestión de tareas.
- [x] Desarrollar interfaz web Kanban interactiva.
- [x] Implementar CLI para operaciones básicas.
- [x] Añadir filtros por proyecto y responsable.

### Fase 2: Mejoras Actuales (En progreso)
- [x] Corrección de errores en actualización de tareas.
- [x] Implementación de filtrado combinado.
- [x] Mejora de la experiencia de usuario en web.
- [ ] Optimización del rendimiento de la base de datos.

### Fase 3: Futuras Mejoras (Planeadas)
- [ ] Integración con autenticación de usuarios.
- [ ] Notificaciones y recordatorios.
- [ ] Exportación de datos en formatos comunes.
- [ ] Integración con reconocimiento de voz.
- [ ] Despliegue en contenedores Docker.
- [ ] API pública para integración con otras herramientas.

## 7. Consideraciones para Despliegue

### 7.1 Despliegue Local
- Requiere Python 3.8+ y dependencias listadas en `requirements.txt`.
- Base de datos SQLite almacenada localmente.

### 7.2 Despliegue en Servidor (Futuro)
- Compatible con despliegue en contenedores Docker.
- Puede escalar a bases de datos más robustas (PostgreSQL, MySQL).
- Arquitectura preparada para autenticación y múltiples usuarios.

## 8. Licencia

Este proyecto está bajo la licencia MIT. Ver el archivo [LICENSE](LICENSE) para más detalles.