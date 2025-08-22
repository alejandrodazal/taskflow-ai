import pytest
from unittest.mock import patch, Mock
from taskflow.kanban.kanban_generator import KanbanGenerator

class TestKanbanGenerator:
    """Tests para KanbanGenerator."""

    @patch('taskflow.kanban.kanban_generator.TaskManager')
    def test_generate_board(self, mock_task_manager):
        """Test generar tablero Kanban."""
        mock_task_manager.return_value.get_tasks.return_value = [
            {'id': 1, 'description': 'Tarea 1', 'status': 'pending', 'priority': 'high'},
            {'id': 2, 'description': 'Tarea 2', 'status': 'pending'},
            {'id': 3, 'description': 'Tarea 3', 'status': 'completed'},
        ]

        generator = KanbanGenerator()
        with patch('taskflow.kanban.kanban_generator.plt'):
            filename = generator.generate_board('Test Project')

        assert filename.startswith('kanban_boards\\kanban_Test_Project_')
        assert filename.endswith('.png')
