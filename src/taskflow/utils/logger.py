import logging
import sys
from pathlib import Path
from typing import Optional
from rich.logging import RichHandler
from taskflow.config import settings

def setup_logger(name: str, level: Optional[str] = None) -> logging.Logger:
    """Configura y retorna un logger con formato rich."""
    
    logger = logging.getLogger(name)
    
    if logger.handlers:
        return logger
    
    log_level = level or settings.log_level
    logger.setLevel(getattr(logging, log_level.upper()))
    
    # Handler para consola con Rich
    console_handler = RichHandler(
        rich_tracebacks=True,
        show_path=False,
        show_time=False
    )
    console_handler.setLevel(logging.INFO)
    
    # Handler para archivo
    file_handler = logging.FileHandler(settings.log_file)
    file_handler.setLevel(logging.DEBUG)
    
    # Formato para archivo
    file_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    file_handler.setFormatter(file_formatter)
    
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    
    return logger

def get_logger(name: str) -> logging.Logger:
    """Obtiene un logger configurado."""
    return setup_logger(name)