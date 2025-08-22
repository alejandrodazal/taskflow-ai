from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field
from typing import Optional, List
import os
from pathlib import Path

class Settings(BaseSettings):
    """Configuración global de la aplicación."""
    
    # GitHub settings
    github_token: str = Field(..., env="GITHUB_TOKEN")
    github_repo: str = Field(..., env="GITHUB_REPO")
    github_username: str = Field(..., env="GITHUB_USERNAME")
    
    # AI settings - Gemini
    llm_provider: str = Field("gemini", env="LLM_PROVIDER")
    gemini_api_key: str = Field(..., env="GEMINI_API_KEY")
    gemini_model: str = Field("gemini-pro", env="GEMINI_MODEL")
    
    # Fallback OpenAI (opcional)
    openai_api_key: Optional[str] = Field(None, env="OPENAI_API_KEY")
    openai_model: str = Field("gpt-3.5-turbo", env="OPENAI_MODEL")
    
    # Voice settings
    tts_engine: str = Field("pyttsx3", env="TTS_ENGINE")
    voice_rate: int = Field(200, env="VOICE_RATE")
    voice_volume: float = Field(0.8, env="VOICE_VOLUME")
    voice_language: str = Field("es", env="VOICE_LANGUAGE")
    
    # Kanban settings
    kanban_output_dir: str = Field("./kanban_boards", env="KANBAN_OUTPUT_DIR")
    kanban_auto_open: bool = Field(True, env="KANBAN_AUTO_OPEN")
    
    # Logging settings
    log_level: str = Field("INFO", env="LOG_LEVEL")
    log_file: str = Field("taskflow.log", env="LOG_FILE")
    
    model_config = SettingsConfigDict(env_file=".env", case_sensitive=False)

# Instancia global de configuración
settings = Settings()
