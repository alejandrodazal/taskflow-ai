# TaskFlow AI - Especificación Técnica del Proyecto

## 1. Resumen Ejecutivo

TaskFlow AI es una herramienta de gestión de proyectos para equipos, impulsada por IA. Funciona como una aplicación CLI tradicional y, adicionalmente, ofrece interfaces web interactivas que permiten la interacción por voz y la gestión visual de tareas mediante tableros Kanban.

## 2. Arquitectura del Sistema

### 2.1 Arquitectura General
El sistema se compone de un backend en Python que contiene toda la lógica de negocio (gestión de tareas, IA) y tres interfaces de usuario:
1.  Una CLI tradicional para comandos directos.
2.  Una interfaz web conversacional con reconocimiento de voz.
3.  Una interfaz web Kanban interactiva para gestión visual de tareas.

### 2.2 Arquitectura Web
- **Backend:** Un servidor web ligero (Flask) que expone una API RESTful.
- **Frontend Conversacional:** Una página HTML única (Single Page Application) con JavaScript que utiliza la Web Speech API del navegador para el reconocimiento de voz.
- **Frontend Kanban:** Una página HTML interactiva con funcionalidad de arrastrar y soltar para gestionar tareas visualmente.
- **Comunicación:** Los frontends envían comandos y solicitudes a la API del backend y muestran los resultados recibidos.

## 3. Modelo de Datos y Módulos

(Sin cambios en la estructura de la base de datos)

## 4. Dependencias Clave

Se añaden las siguientes dependencias para la interfaz web:
```
Flask>=2.0.0
Flask-Cors>=3.0.0
```

## 5. Casos de Uso y Comandos

### 5.1 Nuevos Comandos CLI
```bash
# Inicia la interfaz web conversacional del agente de IA
taskflow web

# Inicia la interfaz web interactiva del tablero Kanban
taskflow kanban
```

### 5.2 Flujo de Interacción Web Conversacional
1. El usuario ejecuta `taskflow web`.
2. Se abre una página en el navegador con un botón de micrófono.
3. El usuario hace clic, habla un comando (ej. "muestra el progreso de ana").
4. La interfaz muestra el texto reconocido y la respuesta del agente.

### 5.3 Flujo de Interacción Web Kanban
1. El usuario ejecuta `taskflow kanban` o abre directamente el archivo `kanban_board.html`.
2. Se muestra un tablero Kanban con columnas para tareas pendientes, en progreso y completadas.
3. El usuario puede arrastrar y soltar tareas entre columnas.
4. El usuario puede crear, editar y eliminar tareas mediante formularios modales.
5. Los datos se almacenan localmente en el navegador del usuario.

## 6. Roadmap de Desarrollo

### Fase 1: Gestión por Responsables (Completada)
- [x] Modificado el esquema de la BD para incluir `assignee`.
- [x] Actualizado `TaskManager` para soportar la asignación.
- [x] Actualizada la UI (Kanban) para mostrar al responsable.

### Fase 2: Análisis de Progreso (Completada)
- [x] Implementado `get_progress_summary` en `TaskManager`.
- [x] Añadida la acción `analyze_progress` en el CLI.
- [x] Integrada la consulta de progreso con el agente de IA.

### Fase 3: Agente Activo en Interfaz Web (Completada)
- [x] Actualizar PRD con la nueva arquitectura web.
- [x] Añadir dependencias (Flask, Flask-Cors).
- [x] Crear el servidor web básico con Flask.
- [x] Desarrollar la interfaz de usuario conversacional (HTML/CSS/JS).
- [x] Implementar la lógica de reconocimiento de voz y comunicación con el backend.
- [x] Añadir el comando `taskflow web` para iniciar el servidor.

### Fase 4: Interfaz Kanban Interactiva (Completada)
- [x] Crear interfaz web Kanban independiente con funcionalidad de arrastrar y soltar.
- [x] Implementar creación, edición y eliminación de tareas.
- [x] Añadir almacenamiento local de datos en el navegador.
- [x] Añadir el comando `taskflow kanban` para iniciar la interfaz.
- [x] Crear archivo HTML independiente para uso sin servidor.
