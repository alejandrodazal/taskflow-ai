import matplotlib.pyplot as plt
import matplotlib.patches as patches
from PIL import Image, ImageDraw, ImageFont
from typing import List, Dict, Any, Optional
from pathlib import Path
from datetime import datetime
from taskflow.taskwarrior import TaskManager
from taskflow.utils import get_logger, sanitize_filename
from taskflow.config import settings

class KanbanGenerator:
    """Generador de tableros Kanban visuales."""
    
    def __init__(self):
        self.task_manager = TaskManager()
        self.logger = get_logger(__name__)
        self.output_dir = Path("kanban_boards")
        self.output_dir.mkdir(exist_ok=True)
    
    def generate_board(self, project: Optional[str] = None) -> str:
        """Genera tablero Kanban y retorna nombre del archivo."""
        try:
            # Obtener tareas
            pending_tasks = self.task_manager.get_tasks(project=project, status="pending")
            completed_tasks = self.task_manager.get_tasks(project=project, status="completed")
            
            # Organizar por columnas
            columns = {
                "Por Hacer": [t for t in pending_tasks if t.get('priority') != 'high'],
                "Urgente": [t for t in pending_tasks if t.get('priority') == 'high'],
                "Completado": completed_tasks[:10]  # Últimas 10 completadas
            }
            
            # Generar imagen
            filename = self._create_kanban_image(columns, project)
            
            self.logger.info(f"Tablero Kanban generado: {filename}")
            return filename
            
        except Exception as e:
            self.logger.error(f"Error generando Kanban: {e}")
            return ""
    
    def _create_kanban_image(self, columns: Dict[str, List], project: Optional[str]) -> str:
        """Crea la imagen del tablero Kanban."""
        # Configuración
        fig_width = 16
        fig_height = 12
        fig, ax = plt.subplots(figsize=(fig_width, fig_height))
        
        # Colores
        colors = {
            "Por Hacer": "#E3F2FD",
            "Urgente": "#FFEBEE", 
            "Completado": "#E8F5E8"
        }
        
        # Título
        title = f"Tablero Kanban - {project}" if project else "Tablero Kanban General"
        fig.suptitle(title, fontsize=20, fontweight='bold', y=0.95)
        
        # Dibujar columnas
        col_width = fig_width / len(columns)
        x_positions = [i * col_width for i in range(len(columns))]
        
        for i, (col_name, tasks) in enumerate(columns.items()):
            x = x_positions[i]
            
            # Fondo de columna
            rect = patches.Rectangle(
                (x, 0), col_width - 0.1, fig_height - 1,
                linewidth=2, edgecolor='black', 
                facecolor=colors.get(col_name, '#F5F5F5'),
                alpha=0.3
            )
            ax.add_patch(rect)
            
            # Título de columna
            ax.text(
                x + col_width/2, fig_height - 0.5, col_name,
                ha='center', va='center', fontsize=16, fontweight='bold'
            )
            
            # Tareas
            y_start = fig_height - 2
            task_height = 0.8
            
            for j, task in enumerate(tasks[:8]):  # Máximo 8 tareas por columna
                y = y_start - (j * (task_height + 0.1))
                
                # Caja de tarea
                task_rect = patches.Rectangle(
                    (x + 0.1, y - task_height/2), col_width - 0.3, task_height,
                    linewidth=1, edgecolor='gray',
                    facecolor='white', alpha=0.9
                )
                ax.add_patch(task_rect)
                
                # Texto de tarea
                desc = task.get('description', '')[:40] + ('...' if len(task.get('description', '')) > 40 else '')
                ax.text(
                    x + col_width/2, y, desc,
                    ha='center', va='center', fontsize=10,
                    wrap=True
                )
                
                # Indicador de prioridad
                priority = task.get('priority', 'normal')
                if priority == 'high':
                    priority_color = 'red'
                elif priority == 'low':
                    priority_color = 'green'
                else:
                    priority_color = 'orange'
                
                priority_circle = patches.Circle(
                    (x + 0.2, y + task_height/3), 0.05,
                    color=priority_color
                )
                ax.add_patch(priority_circle)
        
        # Configurar ejes
        ax.set_xlim(0, fig_width)
        ax.set_ylim(0, fig_height)
        ax.set_aspect('equal')
        ax.axis('off')
        
        # Guardar imagen
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        project_name = sanitize_filename(project) if project else "general"
        filename = f"kanban_{project_name}_{timestamp}.png"
        filepath = self.output_dir / filename
        
        plt.tight_layout()
        plt.savefig(filepath, dpi=300, bbox_inches='tight')
        plt.close()
        
        return str(filepath)
    
    def generate_summary_image(self, project: Optional[str] = None) -> str:
        """Genera imagen resumen de estadísticas."""
        try:
            # Obtener estadísticas
            pending = len(self.task_manager.get_tasks(project=project, status="pending"))
            completed = len(self.task_manager.get_tasks(project=project, status="completed"))
            total = pending + completed
            
            # Crear gráfico de dona
            fig, ax = plt.subplots(figsize=(8, 8))
            
            sizes = [completed, pending]
            labels = ['Completadas', 'Pendientes']
            colors = ['#4CAF50', '#FF9800']
            
            wedges, texts, autotexts = ax.pie(
                sizes, labels=labels, colors=colors,
                autopct='%1.1f%%', startangle=90,
                wedgeprops=dict(width=0.5)
            )
            
            # Título
            title = f"Resumen - {project}" if project else "Resumen General"
            ax.set_title(title, fontsize=16, fontweight='bold')
            
            # Texto central
            ax.text(0, 0, f'{total}\nTareas\nTotales', 
                   ha='center', va='center', fontsize=14, fontweight='bold')
            
            # Guardar
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            project_name = sanitize_filename(project) if project else "general"
            filename = f"summary_{project_name}_{timestamp}.png"
            filepath = self.output_dir / filename
            
            plt.savefig(filepath, dpi=300, bbox_inches='tight')
            plt.close()
            
            return str(filepath)
            
        except Exception as e:
            self.logger.error(f"Error generando resumen: {e}")
            return ""