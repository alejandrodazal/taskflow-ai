# TaskFlow AI - Especificación Técnica del Proyecto

## 1. Resumen Ejecutivo

TaskFlow AI es una herramienta CLI desarrollada en Python que integra inteligencia artificial con Taskwarrior y GitHub para gestión de proyectos personales. Incluye síntesis de voz y generación de tableros Kanban visuales.

## 2. Arquitectura del Sistema

### 2.1 Estructura del Proyecto
```
taskflow-ai/
├── src/
│   ├── taskflow/
│   │   ├── __init__.py
│   │   ├── cli/
│   │   │   ├── __init__.py
│   │   │   ├── main.py
│   │   │   └── commands.py
│   │   ├── ai/
│   │   │   ├── __init__.py
│   │   │   ├── llm_client.py
│   │   │   └── prompt_templates.py
│   │   ├── taskwarrior/
│   │   │   ├── __init__.py
│   │   │   ├── task_manager.py
│   │   │   └── task_parser.py
│   │   ├── github/
│   │   │   ├── __init__.py
│   │   │   ├── github_client.py
│   │   │   └── sync_manager.py
│   │   ├── voice/
│   │   │   ├── __init__.py
│   │   │   └── tts_engine.py
│   │   ├── kanban/
│   │   │   ├── __init__.py
│   │   │   ├── board_generator.py
│   │   │   └── image_renderer.py
│   │   ├── config/
│   │   │   ├── __init__.py
│   │   │   └── settings.py
│   │   └── utils/
│   │       ├── __init__.py
│   │       ├── logger.py
│   │       └── helpers.py
├── tests/
│   ├── unit/
│   ├── integration/
│   └── fixtures/
├── docs/
├── requirements.txt
├── setup.py
├── README.md
├── .env.example
└── config.yaml.example
```

### 2.2 Dependencias Principales

```python:requirements.txt
# Core dependencies
click>=8.0.0
pydantic>=2.0.0
pyyaml>=6.0
requests>=2.28.0

# AI/LLM integration
openai>=1.0.0
langchain>=0.1.0
transformers>=4.30.0

# GitHub integration
PyGithub>=1.58.0

# Taskwarrior integration
taskw>=1.3.1

# Voice synthesis
pyttsx3>=2.90
gTTS>=2.3.0

# Image generation for Kanban
Pillow>=9.0.0
matplotlib>=3.6.0
seaborn>=0.12.0

# Development and testing
pytest>=7.0.0
pytest-cov>=4.0.0
black>=22.0.0
flake8>=5.0.0
mypy>=1.0.0
```

## 3. Especificaciones de Módulos

### 3.1 CLI Module (src/taskflow/cli/)

**main.py**
```python
import click
from taskflow.ai.llm_client import LLMClient
from taskflow.taskwarrior.task_manager import TaskManager
from taskflow.github.sync_manager import SyncManager
from taskflow.voice.tts_engine import TTSEngine
from taskflow.kanban.board_generator import KanbanGenerator

@click.group()
@click.pass_context
def cli(ctx):
    """TaskFlow AI - Gestión inteligente de tareas"""
    ctx.ensure_object(dict)
    ctx.obj['task_manager'] = TaskManager()
    ctx.obj['llm_client'] = LLMClient()
    ctx.obj['sync_manager'] = SyncManager()
    ctx.obj['tts_engine'] = TTSEngine()
    ctx.obj['kanban_generator'] = KanbanGenerator()

@cli.command()
@click.argument('query', required=True)
@click.option('--voice', '-v', is_flag=True, help='Respuesta por voz')
@click.pass_context
def ask(ctx, query: str, voice: bool):
    """Procesar comando en lenguaje natural"""
    # Implementación del comando principal
    pass
```

### 3.2 AI Module (src/taskflow/ai/)

**llm_client.py**
```python
from typing import Dict, Any, Optional
from abc import ABC, abstractmethod
import openai
from langchain.llms import OpenAI
from taskflow.config.settings import Settings

class LLMProvider(ABC):
    @abstractmethod
    def generate_response(self, prompt: str, context: Dict[str, Any]) -> str:
        pass

class OpenAIProvider(LLMProvider):
    def __init__(self, api_key: str, model: str = "gpt-3.5-turbo"):
        self.client = openai.OpenAI(api_key=api_key)
        self.model = model
    
    def generate_response(self, prompt: str, context: Dict[str, Any]) -> str:
        # Implementación de OpenAI
        pass

class LocalLLMProvider(LLMProvider):
    def __init__(self, model_path: str):
        # Implementación para modelos locales (Ollama, etc.)
        pass

class LLMClient:
    def __init__(self):
        self.settings = Settings()
        self.provider = self._initialize_provider()
    
    def interpret_command(self, user_input: str) -> Dict[str, Any]:
        """Interpreta comando en lenguaje natural y retorna acción estructurada"""
        pass
    
    def generate_task_list(self, project_description: str) -> List[Dict[str, Any]]:
        """Genera lista de tareas basada en descripción del proyecto"""
        pass
```

### 3.3 TaskWarrior Module (src/taskflow/taskwarrior/)

**task_manager.py**
```python
from taskw import TaskWarrior
from typing import List, Dict, Any, Optional
from datetime import datetime
from taskflow.utils.logger import get_logger

class TaskManager:
    def __init__(self):
        self.tw = TaskWarrior()
        self.logger = get_logger(__name__)
    
    def create_project(self, name: str, description: str = "") -> str:
        """Crea un nuevo proyecto"""
        pass
    
    def add_task(self, description: str, project: str = None, 
                 priority: str = None, due: datetime = None) -> Dict[str, Any]:
        """Añade una nueva tarea"""
        pass
    
    def update_task(self, task_id: str, **kwargs) -> Dict[str, Any]:
        """Actualiza una tarea existente"""
        pass
    
    def complete_task(self, task_id: str) -> Dict[str, Any]:
        """Marca una tarea como completada"""
        pass
    
    def get_tasks(self, project: str = None, status: str = "pending") -> List[Dict[str, Any]]:
        """Obtiene lista de tareas"""
        pass
    
    def get_projects(self) -> List[str]:
        """Obtiene lista de proyectos"""
        pass
```

### 3.4 GitHub Integration Module (src/taskflow/github/)

**github_client.py**
```python
from github import Github
from typing import Dict, Any, Optional
from taskflow.config.settings import Settings

class GitHubClient:
    def __init__(self):
        self.settings = Settings()
        self.client = Github(self.settings.github_token)
        self.repo = self.client.get_repo(self.settings.github_repo)
    
    def create_issue(self, title: str, body: str, labels: List[str] = None) -> Dict[str, Any]:
        """Crea un issue en GitHub"""
        pass
    
    def update_issue(self, issue_number: int, **kwargs) -> Dict[str, Any]:
        """Actualiza un issue existente"""
        pass
    
    def close_issue(self, issue_number: int) -> Dict[str, Any]:
        """Cierra un issue"""
        pass

**sync_manager.py**
```python
class SyncManager:
    def __init__(self):
        self.github_client = GitHubClient()
        self.task_manager = TaskManager()
    
    def sync_task_to_github(self, task: Dict[str, Any]) -> Optional[int]:
        """Sincroniza tarea de Taskwarrior a GitHub"""
        pass
    
    def sync_all_tasks(self) -> Dict[str, Any]:
        """Sincroniza todas las tareas pendientes"""
        pass
```

### 3.5 Voice Module (src/taskflow/voice/)

**tts_engine.py**
```python
import pyttsx3
from gtts import gTTS
import os
import tempfile
from typing import Optional

class TTSEngine:
    def __init__(self, engine_type: str = "pyttsx3"):
        self.engine_type = engine_type
        if engine_type == "pyttsx3":
            self.engine = pyttsx3.init()
            self._configure_voice()
    
    def speak(self, text: str, save_to_file: bool = False) -> Optional[str]:
        """Convierte texto a voz"""
        pass
    
    def _configure_voice(self):
        """Configura parámetros de voz"""
        pass
```

### 3.6 Kanban Module (src/taskflow/kanban/)

**board_generator.py**
```python
from PIL import Image, ImageDraw, ImageFont
import matplotlib.pyplot as plt
from typing import List, Dict, Any
import os

class KanbanGenerator:
    def __init__(self):
        self.board_width = 1200
        self.board_height = 800
        self.column_width = 350
    
    def generate_board(self, project: str) -> str:
        """Genera tablero Kanban para un proyecto"""
        tasks = self._get_project_tasks(project)
        board_data = self._organize_tasks_by_status(tasks)
        image_path = self._create_board_image(board_data, project)
        return image_path
    
    def _create_board_image(self, board_data: Dict[str, List], project: str) -> str:
        """Crea imagen del tablero Kanban"""
        pass
    
    def open_board(self, image_path: str):
        """Abre la imagen del tablero en el visor predeterminado"""
        os.startfile(image_path)  # Windows
        # os.system(f"open {image_path}")  # macOS
        # os.system(f"xdg-open {image_path}")  # Linux
```

### 3.7 Configuration Module (src/taskflow/config/)

**settings.py**
```python
from pydantic import BaseSettings, Field
from typing import Optional
import os

class Settings(BaseSettings):
    # GitHub settings
    github_token: str = Field(..., env="GITHUB_TOKEN")
    github_repo: str = Field(..., env="GITHUB_REPO")
    
    # AI settings
    llm_provider: str = Field("openai", env="LLM_PROVIDER")
    openai_api_key: Optional[str] = Field(None, env="OPENAI_API_KEY")
    local_model_path: Optional[str] = Field(None, env="LOCAL_MODEL_PATH")
    
    # Voice settings
    tts_engine: str = Field("pyttsx3", env="TTS_ENGINE")
    voice_rate: int = Field(200, env="VOICE_RATE")
    voice_volume: float = Field(0.8, env="VOICE_VOLUME")
    
    # Kanban settings
    kanban_output_dir: str = Field("./kanban_boards", env="KANBAN_OUTPUT_DIR")
    
    class Config:
        env_file = ".env"
        case_sensitive = False
```

## 4. Configuración del Proyecto

### 4.1 setup.py
```python
from setuptools import setup, find_packages

setup(
    name="taskflow-ai",
    version="1.1.0",
    description="Herramienta CLI con IA para gestión de tareas con Taskwarrior y GitHub",
    author="Tu Nombre",
    author_email="tu.email@ejemplo.com",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "click>=8.0.0",
        "pydantic>=2.0.0",
        "pyyaml>=6.0",
        "requests>=2.28.0",
        "PyGithub>=1.58.0",
        "taskw>=1.3.1",
        "pyttsx3>=2.90",
        "Pillow>=9.0.0",
        "matplotlib>=3.6.0",
    ],
    extras_require={
        "openai": ["openai>=1.0.0"],
        "local-llm": ["transformers>=4.30.0", "torch>=2.0.0"],
        "dev": ["pytest>=7.0.0", "black>=22.0.0", "flake8>=5.0.0"],
    },
    entry_points={
        "console_scripts": [
            "taskflow=taskflow.cli.main:cli",
        ],
    },
    python_requires=">=3.8",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
)
```

### 4.2 Archivo de configuración (.env.example)
```bash
# GitHub Configuration
GITHUB_TOKEN=your_github_personal_access_token
GITHUB_REPO=username/repository-name

# AI Configuration
LLM_PROVIDER=openai  # opciones: openai, local
OPENAI_API_KEY=your_openai_api_key
LOCAL_MODEL_PATH=/path/to/local/model

# Voice Configuration
TTS_ENGINE=pyttsx3  # opciones: pyttsx3, gtts
VOICE_RATE=200
VOICE_VOLUME=0.8

# Kanban Configuration
KANBAN_OUTPUT_DIR=./kanban_boards
```

## 5. Casos de Uso y Comandos

### 5.1 Comandos CLI Principales
```bash
# Crear proyecto
taskflow ask "Crea un proyecto llamado 'Website Redesign' para rediseñar nuestro sitio web"

# Añadir tareas
taskflow ask "Añade tareas para el proyecto Website Redesign: investigar competencia, crear wireframes, desarrollar frontend"

# Ver estado con voz
taskflow ask "¿Cuáles son mis tareas pendientes?" --voice

# Generar tablero Kanban
taskflow ask "Genera un tablero Kanban para el proyecto Website Redesign"

# Completar tarea
taskflow ask "Marca como completada la tarea de investigar competencia"
```

## 6. Testing Strategy

### 6.1 Estructura de Tests
```python
# tests/unit/test_task_manager.py
import pytest
from taskflow.taskwarrior.task_manager import TaskManager

class TestTaskManager:
    def test_create_project(self):
        pass
    
    def test_add_task(self):
        pass

# tests/integration/test_github_sync.py
class TestGitHubSync:
    def test_sync_task_to_github(self):
        pass
```

## 7. Deployment y Distribución

### 7.1 Instalación
```bash
# Instalación desde PyPI (futuro)
pip install taskflow-ai

# Instalación desde código fuente
git clone https://github.com/usuario/taskflow-ai.git
cd taskflow-ai
pip install -e .

# Configuración inicial
cp .env.example .env
# Editar .env con tus tokens y configuraciones

# Verificar instalación
taskflow --help
```

## 8. Roadmap de Desarrollo

### Fase 1: Core Functionality
- [ ] CLI básico con Click
- [ ] Integración con TaskWarrior
- [ ] Cliente LLM básico
- [ ] Comandos de gestión de tareas

### Fase 2: GitHub Integration
- [ ] Cliente GitHub
- [ ] Sincronización unidireccional
- [ ] Manejo de errores y reintentos

### Fase 3: Voice & Kanban
- [ ] Motor TTS
- [ ] Generador de tableros Kanban
- [ ] Visualización de imágenes

### Fase 4: Polish & Testing
- [ ] Tests completos
- [ ] Documentación
- [ ] Empaquetado para distribución

## 9. Consideraciones de Implementación

### 9.1 Manejo de Errores
- Implementar logging robusto
- Manejo de fallos de red (GitHub API)
- Validación de entrada del usuario
- Fallbacks para servicios externos

### 9.2 Performance
- Cache de respuestas LLM frecuentes
- Procesamiento asíncrono para operaciones lentas
- Optimización de generación de imágenes

### 9.3 Seguridad
- Almacenamiento seguro de tokens
- Validación de entrada para prevenir inyecciones
- Manejo seguro de archivos temporales
```

Esta especificación técnica transforma el PRD original en un documento completamente implementable como proyecto Python, incluyendo:

1. **Arquitectura modular** con separación clara de responsabilidades
2. **Estructura de proyecto** estándar de Python
3. **Especificaciones de código** con ejemplos concretos
4. **Dependencias específicas** y sus versiones
5. **Configuración del proyecto** (setup.py, requirements.txt)
6. **Estrategia de testing** y estructura de pruebas
7. **Plan de deployment** y distribución
8. **Roadmap de desarrollo** por fases

El proyecto está listo para comenzar la implementación siguiendo las mejores prácticas de desarrollo Python.
        