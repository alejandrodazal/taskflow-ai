import pytest
from unittest.mock import Mock, patch
from taskflow.voice.tts_engine import TTSEngine

class TestTTSEngine:
    """Tests para TTSEngine."""
    
    @patch('taskflow.voice.tts_engine.pyttsx3')
    def test_speak_pyttsx3(self, mock_pyttsx3):
        """Test síntesis de voz con pyttsx3."""
        mock_engine = Mock()
        mock_pyttsx3.init.return_value = mock_engine
        
        tts = TTSEngine()
        tts.speak("Texto de prueba", use_gtts=False)
        
        mock_engine.say.assert_called_once_with("Texto de prueba")
        mock_engine.runAndWait.assert_called_once()
    
    @patch('taskflow.voice.tts_engine.gTTS')
    @patch('taskflow.voice.tts_engine.pygame')
    def test_speak_gtts(self, mock_pygame, mock_gtts):
        """Test síntesis de voz con gTTS."""
        mock_tts_obj = Mock()
        mock_gtts.return_value = mock_tts_obj
        
        tts = TTSEngine()
        tts.speak("Texto de prueba", use_gtts=True)
        
        mock_gtts.assert_called_once_with(text="Texto de prueba", lang='es', slow=False)
        mock_tts_obj.save.assert_called_once()