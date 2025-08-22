import pytest
import json
from unittest.mock import Mock, patch, MagicMock
from taskflow.ai.llm_client import LLMClient, GeminiProvider, OpenAIProvider

class TestGeminiProvider:
    """Tests para GeminiProvider."""
    
    @patch('taskflow.ai.llm_client.genai')
    def test_generate_response_success(self, mock_genai):
        """Test generar respuesta exitosamente."""
        mock_model = Mock()
        mock_model.generate_content.return_value.text = "Respuesta de prueba"
        mock_genai.GenerativeModel.return_value = mock_model
        
        provider = GeminiProvider("test_key")
        response = provider.generate_response("Test prompt")
        
        assert response == "Respuesta de prueba"
        mock_model.generate_content.assert_called_once()
    
    @patch('taskflow.ai.llm_client.genai')
    def test_generate_response_with_context(self, mock_genai):
        """Test generar respuesta con contexto."""
        mock_model = Mock()
        mock_model.generate_content.return_value.text = "Respuesta con contexto"
        mock_genai.GenerativeModel.return_value = mock_model
        
        provider = GeminiProvider("test_key")
        context = {"tasks": ["tarea1", "tarea2"]}
        response = provider.generate_response("Test prompt", context)
        
        assert response == "Respuesta con contexto"
        # Verificar que el contexto se incluyó en el prompt
        call_args = mock_model.generate_content.call_args[0][0]
        assert "Contexto actual:" in call_args

class TestLLMClient:
    """Tests para LLMClient."""
    
    @patch('taskflow.ai.llm_client.settings')
    @patch('taskflow.ai.llm_client.genai')
    def test_interpret_command_create_task(self, mock_genai, mock_settings):
        """Test interpretar comando de crear tarea."""
        mock_settings.gemini_api_key = "test_key"
        mock_settings.gemini_model = "gemini-pro"
        mock_settings.llm_provider = "gemini"
        
        mock_model = Mock()
        mock_response = {
            "action": "create_task",
            "details": {
                "description": "Nueva tarea de prueba",
                "priority": "medium"
            }
        }
        mock_model.generate_content.return_value.text = json.dumps(mock_response)
        mock_genai.GenerativeModel.return_value = mock_model
        
        client = LLMClient()
        result = client.interpret_command("Crear una nueva tarea de prueba")
        
        assert result["action"] == "create_task"
        assert result["details"]["description"] == "Nueva tarea de prueba"
    
    @patch('taskflow.ai.llm_client.settings')
    @patch('taskflow.ai.llm_client.genai')
    def test_generate_task_list(self, mock_genai, mock_settings):
        """Test generar lista de tareas."""
        mock_settings.gemini_api_key = "test_key"
        mock_settings.gemini_model = "gemini-pro"
        mock_settings.llm_provider = "gemini"
        
        mock_model = Mock()
        mock_tasks = [
            {"description": "Tarea 1", "priority": "high"},
            {"description": "Tarea 2", "priority": "medium"}
        ]
        mock_model.generate_content.return_value.text = json.dumps(mock_tasks)
        mock_genai.GenerativeModel.return_value = mock_model
        
        client = LLMClient()
        tasks = client.generate_task_list("Proyecto de prueba")
        
        assert len(tasks) == 2
        assert tasks[0]["description"] == "Tarea 1"
        assert tasks[1]["priority"] == "medium"