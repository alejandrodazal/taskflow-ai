from flask import Flask, render_template, request, jsonify
from kanban_app.database import init_db, get_session
from kanban_app.models import Task, Project, Assignee, TaskStatus, Priority
import os

def create_app():
    app = Flask(__name__, 
                template_folder=os.path.dirname(os.path.abspath(__file__)),
                static_folder=os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static'))
    
    # Inicializar la base de datos
    init_db()
    
    @app.route('/')
    def kanban_board():
        """Sirve la página principal del tablero Kanban"""
        return render_template('kanban_board.html')
    
    @app.route('/favicon.ico')
    def favicon():
        """Servir favicon"""
        return '', 204
    
    @app.route('/api/tasks', methods=['GET'])
    def get_tasks():
        """Obtener todas las tareas"""
        try:
            db = get_session()
            
            # Obtener parámetros de filtro
            project_filter = request.args.get('project')
            assignee_filter = request.args.get('assignee')
            
            print(f"Filtros recibidos - Proyecto: {project_filter}, Responsable: {assignee_filter}")  # Para debugging
            
            # Construir consulta
            query = db.query(Task)
            
            # Aplicar filtro por proyecto si se especifica
            if project_filter:
                project = db.query(Project).filter(Project.name == project_filter).first()
                print(f"Proyecto encontrado: {project}")  # Para debugging
                if project:
                    query = query.filter(Task.project_id == project.id)
                else:
                    # Si el proyecto no existe, devolver lista vacía
                    print("Proyecto no encontrado, devolviendo lista vacía")  # Para debugging
                    return jsonify([])
            
            # Aplicar filtro por responsable si se especifica
            if assignee_filter:
                assignee = db.query(Assignee).filter(Assignee.name == assignee_filter).first()
                print(f"Responsable encontrado: {assignee}")  # Para debugging
                if assignee:
                    query = query.filter(Task.assignee_id == assignee.id)
                else:
                    # Si el responsable no existe, devolver lista vacía
                    print("Responsable no encontrado, devolviendo lista vacía")  # Para debugging
                    return jsonify([])
            
            tasks = query.all()
            print(f"Tareas encontradas: {len(tasks)}")  # Para debugging
            return jsonify([task.to_dict() for task in tasks])
        except Exception as e:
            print(f"Error al obtener tareas: {str(e)}")  # Para debugging
            return jsonify({'error': str(e)}), 500
        finally:
            db.close()
    
    @app.route('/api/tasks', methods=['POST'])
    def create_task():
        """Crear una nueva tarea"""
        try:
            data = request.get_json()
            if not data:
                return jsonify({'error': 'Datos inválidos'}), 400
            
            db = get_session()
            
            # Buscar o crear proyecto
            project_id = None
            if data.get('project_name'):
                project = db.query(Project).filter(Project.name == data['project_name']).first()
                if not project:
                    project = Project(name=data['project_name'])
                    db.add(project)
                    db.commit()
                    db.refresh(project)
                project_id = project.id
            
            # Buscar o crear responsable
            assignee_id = None
            if data.get('assignee_name'):
                assignee = db.query(Assignee).filter(Assignee.name == data['assignee_name']).first()
                if not assignee:
                    assignee = Assignee(name=data['assignee_name'])
                    db.add(assignee)
                    db.commit()
                    db.refresh(assignee)
                assignee_id = assignee.id
            
            # Validar prioridad
            priority = Priority.MEDIUM
            if data.get('priority'):
                try:
                    priority = Priority(data['priority'])
                except ValueError:
                    pass  # Usar valor por defecto
            
            # Validar estado
            status = TaskStatus.PENDING
            if data.get('status'):
                try:
                    status = TaskStatus(data['status'])
                except ValueError:
                    pass  # Usar valor por defecto
            
            task = Task(
                title=data.get('title', ''),
                description=data.get('description', ''),
                project_id=project_id,
                assignee_id=assignee_id,
                priority=priority,
                status=status
            )
            
            db.add(task)
            db.commit()
            db.refresh(task)
            
            return jsonify(task.to_dict()), 201
        except Exception as e:
            db.rollback()
            print(f"Error al crear tarea: {str(e)}")  # Para debugging
            return jsonify({'error': str(e)}), 500
        finally:
            db.close()
    
    @app.route('/api/tasks/<int:task_id>', methods=['PUT'])
    def update_task(task_id):
        """Actualizar una tarea existente"""
        try:
            data = request.get_json()
            if not data:
                return jsonify({'error': 'Datos inválidos'}), 400
            
            db = get_session()
            
            task = db.query(Task).filter(Task.id == task_id).first()
            if not task:
                return jsonify({'error': 'Tarea no encontrada'}), 404
            
            print(f"Actualizando tarea {task_id} con datos: {data}")  # Para debugging
            
            # Actualizar campos
            if 'title' in data:
                task.title = data['title']
            if 'description' in data:
                task.description = data['description']
            
            # Actualizar proyecto
            if 'project_name' in data:
                if data['project_name']:
                    project = db.query(Project).filter(Project.name == data['project_name']).first()
                    if not project:
                        project = Project(name=data['project_name'])
                        db.add(project)
                        db.commit()
                        db.refresh(project)
                    task.project_id = project.id
                else:
                    task.project_id = None
            
            # Actualizar responsable
            if 'assignee_name' in data:
                if data['assignee_name']:
                    assignee = db.query(Assignee).filter(Assignee.name == data['assignee_name']).first()
                    if not assignee:
                        assignee = Assignee(name=data['assignee_name'])
                        db.add(assignee)
                        db.commit()
                        db.refresh(assignee)
                    task.assignee_id = assignee.id
                else:
                    task.assignee_id = None
            
            # Validar y actualizar prioridad
            if 'priority' in data:
                try:
                    task.priority = Priority(data['priority'])
                except ValueError:
                    pass  # Mantener valor actual
            
            # Validar y actualizar estado
            if 'status' in data:
                try:
                    task.status = TaskStatus(data['status'])
                except ValueError:
                    pass  # Mantener valor actual
            
            # Actualizar la fecha de modificación
            from datetime import datetime
            task.updated_at = datetime.utcnow()
            db.commit()
            
            return jsonify(task.to_dict())
        except Exception as e:
            db.rollback()
            print(f"Error al actualizar tarea {task_id}: {str(e)}")  # Para debugging
            return jsonify({'error': str(e)}), 500
        finally:
            db.close()
    
    @app.route('/api/tasks/<int:task_id>', methods=['DELETE'])
    def delete_task(task_id):
        """Eliminar una tarea"""
        try:
            db = get_session()
            
            task = db.query(Task).filter(Task.id == task_id).first()
            if not task:
                return jsonify({'error': 'Tarea no encontrada'}), 404
            
            db.delete(task)
            db.commit()
            
            return jsonify({'message': 'Tarea eliminada correctamente'})
        except Exception as e:
            db.rollback()
            return jsonify({'error': str(e)}), 500
        finally:
            db.close()
    
    @app.route('/api/tasks/<int:task_id>/status', methods=['PUT'])
    def update_task_status(task_id):
        """Actualizar el estado de una tarea"""
        try:
            data = request.get_json()
            if not data or 'status' not in data:
                return jsonify({'error': 'Datos inválidos'}), 400
            
            db = get_session()
            
            task = db.query(Task).filter(Task.id == task_id).first()
            if not task:
                return jsonify({'error': 'Tarea no encontrada'}), 404
            
            # Validar que el estado sea válido
            try:
                task.status = TaskStatus(data['status'])
            except ValueError:
                return jsonify({'error': 'Estado inválido'}), 400
            
            # Actualizar la fecha de modificación
            from datetime import datetime
            task.updated_at = datetime.utcnow()
            db.commit()
            
            return jsonify(task.to_dict())
        except Exception as e:
            db.rollback()
            print(f"Error al actualizar tarea {task_id}: {str(e)}")  # Para debugging
            return jsonify({'error': str(e)}), 500
        finally:
            db.close()
    
    @app.route('/api/projects', methods=['GET'])
    def get_projects():
        """Obtener todos los proyectos"""
        try:
            db = get_session()
            projects = db.query(Project).all()
            return jsonify([project.to_dict() for project in projects])
        except Exception as e:
            return jsonify({'error': str(e)}), 500
        finally:
            db.close()
    
    @app.route('/api/assignees', methods=['GET'])
    def get_assignees():
        """Obtener todos los responsables"""
        try:
            db = get_session()
            assignees = db.query(Assignee).all()
            return jsonify([assignee.to_dict() for assignee in assignees])
        except Exception as e:
            return jsonify({'error': str(e)}), 500
        finally:
            db.close()
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, port=5002)