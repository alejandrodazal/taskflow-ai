import pytest
from unittest.mock import patch, Mock
from taskflow.taskwarrior.task_manager import TaskManager
from taskflow.ai.llm_client import LLMClient
from taskflow.github.sync_manager import SyncManager

class TestWorkflowIntegration:
    """Tests de integración del flujo completo."""

    @patch('taskflow.taskwarrior.task_manager.TaskWarrior')
    @patch('taskflow.ai.llm_client.genai')
    @patch('taskflow.github.github_client.Github')
    def test_complete_workflow(self, mock_github, mock_genai, mock_taskwarrior):
        """Test flujo completo: comando -> tarea -> GitHub."""
        # Mock TaskManager
        mock_task_instance = mock_taskwarrior.return_value
        mock_task_instance.task_add.return_value = {
            'id': 1,
            'uuid': 'test-uuid',
            'description': 'Implementar nueva funcionalidad',
            'project': 'test_project',
            'priority': 'H',
            'tags': ['test']
        }

        # Mock LLMClient
        mock_model = Mock()
        mock_model.generate_content.return_value.text = '''{
            "title": "Implementar nueva funcionalidad",
            "body": "Descripción detallada de la tarea."
        }'''
        mock_genai.GenerativeModel.return_value = mock_model

        # Mock GitHub
        mock_repo = Mock()
        mock_issue = Mock()
        mock_issue.number = 456
        mock_issue.html_url = "https://github.com/test/repo/issues/456"
        mock_repo.create_issue.return_value = mock_issue
        mock_github.return_value.get_repo.return_value = mock_repo

        # Ejecutar flujo
        task_manager = TaskManager()
        llm_client = LLMClient()
        sync_manager = SyncManager()

        # 1. Crear tarea
        task = task_manager.add_task(
            description='Implementar nueva funcionalidad',
            project='test_project',
            priority='H',
            tags=['test']
        )

        # 2. Sincronizar con GitHub
        issue_number = sync_manager.sync_task_to_github(task)

        assert issue_number == 456
