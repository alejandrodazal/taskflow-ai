import pyttsx3
from gtts import gTTS
import pygame
import tempfile
import os
from typing import Optional
from taskflow.utils import get_logger
from taskflow.config import settings

class TTSEngine:
    """Motor de síntesis de texto a voz."""
    
    def __init__(self):
        self.logger = get_logger(__name__)
        self.engine = None
        self._init_pyttsx3()
    
    def _init_pyttsx3(self):
        """Inicializa el motor pyttsx3."""
        try:
            self.engine = pyttsx3.init()
            # Configurar velocidad y voz
            self.engine.setProperty('rate', 150)
            voices = self.engine.getProperty('voices')
            if voices:
                # Buscar voz en español
                for voice in voices:
                    if 'spanish' in voice.name.lower() or 'es' in voice.id.lower():
                        self.engine.setProperty('voice', voice.id)
                        break
        except Exception as e:
            self.logger.warning(f"No se pudo inicializar pyttsx3: {e}")
            self.engine = None
    
    def speak(self, text: str, use_gtts: bool = False) -> bool:
        """Convierte texto a voz."""
        try:
            if use_gtts or not self.engine:
                return self._speak_with_gtts(text)
            else:
                return self._speak_with_pyttsx3(text)
        except Exception as e:
            self.logger.error(f"Error en síntesis de voz: {e}")
            return False
    
    def _speak_with_pyttsx3(self, text: str) -> bool:
        """Usa pyttsx3 para síntesis local."""
        try:
            if not self.engine:
                return False
            
            self.engine.say(text)
            self.engine.runAndWait()
            return True
        except Exception as e:
            self.logger.error(f"Error con pyttsx3: {e}")
            return False
    
    def _speak_with_gtts(self, text: str) -> bool:
        """Usa gTTS para síntesis online."""
        try:
            # Crear archivo temporal
            with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as tmp_file:
                tmp_filename = tmp_file.name
            
            # Generar audio con gTTS
            tts = gTTS(text=text, lang='es', slow=False)
            tts.save(tmp_filename)
            
            # Reproducir con pygame
            pygame.mixer.init()
            pygame.mixer.music.load(tmp_filename)
            pygame.mixer.music.play()
            
            # Esperar a que termine
            while pygame.mixer.music.get_busy():
                pygame.time.wait(100)
            
            # Limpiar
            pygame.mixer.quit()
            os.unlink(tmp_filename)
            
            return True
            
        except Exception as e:
            self.logger.error(f"Error con gTTS: {e}")
            return False
    
    def get_available_voices(self) -> list:
        """Obtiene lista de voces disponibles."""
        if not self.engine:
            return []
        
        try:
            voices = self.engine.getProperty('voices')
            return [{'id': v.id, 'name': v.name} for v in voices]
        except:
            return []