import re
import json
from datetime import datetime, timedelta
from typing import Dict, Any, Optional, List
from pathlib import Path

def sanitize_filename(filename: str) -> str:
    """Sanitiza un nombre de archivo removiendo caracteres inválidos."""
    return re.sub(r'[<>:"/\\|?*]', '_', filename)

def parse_natural_date(date_str: str) -> Optional[datetime]:
    """Parsea fechas en lenguaje natural a datetime."""
    date_str = date_str.lower().strip()
    now = datetime.now()
    
    if date_str in ['hoy', 'today']:
        return now
    elif date_str in ['mañana', 'tomorrow']:
        return now + timedelta(days=1)
    elif date_str in ['próxima semana', 'next week']:
        return now + timedelta(weeks=1)
    elif date_str in ['próximo mes', 'next month']:
        return now + timedelta(days=30)
    
    # Intentar parsear formato ISO
    try:
        return datetime.fromisoformat(date_str)
    except ValueError:
        pass
    
    return None

def format_task_for_display(task: Dict[str, Any]) -> str:
    """Formatea una tarea para mostrar en consola."""
    status_emoji = {
        'pending': '⏳',
        'completed': '✅',
        'deleted': '❌',
        'waiting': '⏸️'
    }
    
    emoji = status_emoji.get(task.get('status', 'pending'), '❓')
    description = task.get('description', 'Sin descripción')
    project = task.get('project', '')
    priority = task.get('priority', '')
    
    result = f"{emoji} {description}"
    
    if project:
        result += f" [{project}]"
    
    if priority:
        result += f" (Prioridad: {priority})"
    
    return result

def save_json(data: Dict[str, Any], filepath: Path) -> None:
    """Guarda datos en formato JSON."""
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False, default=str)

def load_json(filepath: Path) -> Dict[str, Any]:
    """Carga datos desde un archivo JSON."""
    if not filepath.exists():
        return {}
    
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)