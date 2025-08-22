import pytest
from unittest.mock import patch, Mock
from taskflow.taskwarrior.task_manager import TaskManager

class TestTaskManager:
    """Tests para TaskManager."""

    @patch('taskflow.taskwarrior.task_manager.TaskWarrior')
    def test_add_task(self, mock_taskwarrior):
        """Test añadir una nueva tarea."""
        mock_instance = mock_taskwarrior.return_value
        mock_instance.task_add.return_value = {'id': 1, 'description': 'Nueva tarea'}

        manager = TaskManager()
        task = manager.add_task('Nueva tarea')

        assert task['id'] == 1
        assert task['description'] == 'Nueva tarea'
        mock_instance.task_add.assert_called_once_with(description='Nueva tarea')

    @patch('taskflow.taskwarrior.task_manager.TaskWarrior')
    def test_get_tasks(self, mock_taskwarrior):
        """Test obtener lista de tareas."""
        mock_instance = mock_taskwarrior.return_value
        mock_instance.load_tasks.return_value = {
            'pending': [{'id': 1, 'description': 'Tarea pendiente'}],
            'completed': [],
        }

        manager = TaskManager()
        tasks = manager.get_tasks()

        assert len(tasks) == 1
        assert tasks[0]['description'] == 'Tarea pendiente'

    @patch('taskflow.taskwarrior.task_manager.TaskWarrior')
    def test_complete_task(self, mock_taskwarrior):
        """Test completar una tarea."""
        mock_instance = mock_taskwarrior.return_value
        mock_instance.task_done.return_value = {'id': 1, 'status': 'completed'}

        manager = TaskManager()
        task = manager.complete_task(1)

        assert task['status'] == 'completed'
        mock_instance.task_done.assert_called_once_with(1)
