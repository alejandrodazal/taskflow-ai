import pytest
import os
import tempfile
import shutil
from unittest.mock import Mock, patch
from taskflow.config import Settings
from taskflow.taskwarrior.task_manager import TaskManager
from taskflow.ai.llm_client import LLMClient
from taskflow.github.github_client import GitHubClient

@pytest.fixture
def temp_dir():
    """Directorio temporal para tests."""
    temp_path = tempfile.mkdtemp()
    yield temp_path
    shutil.rmtree(temp_path)

@pytest.fixture
def mock_settings():
    """Configuración mock para tests."""
    return Settings(
        taskwarrior_data_location="/tmp/taskwarrior",
        github_token="test_token",
        github_repo="test/repo",
        gemini_api_key="test_key",
        gemini_model="gemini-pro",
        voice_enabled=True,
        voice_engine="pyttsx3",
        kanban_output_dir="/tmp/kanban"
    )

@pytest.fixture
def mock_task_manager(mock_settings):
    """TaskManager mock."""
    with patch('taskflow.taskwarrior.task_manager.subprocess') as mock_subprocess:
        mock_subprocess.run.return_value.returncode = 0
        mock_subprocess.run.return_value.stdout = '{"id": 1, "description": "Test task"}'
        yield TaskManager()

@pytest.fixture
def mock_llm_client():
    """LLMClient mock."""
    with patch('taskflow.ai.llm_client.genai'):
        yield LLMClient()

@pytest.fixture
def mock_github_client(mock_settings):
    """GitHubClient mock."""
    with patch('taskflow.github.github_client.Github'):
        yield GitHubClient("test_token", "test/repo")