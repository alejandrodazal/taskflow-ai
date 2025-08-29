import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from kanban_app.models import Base

# Directorio para la base de datos
basedir = os.path.abspath(os.path.dirname(__file__))

# URL de la base de datos
SQLALCHEMY_DATABASE_URL = f"sqlite:///{os.path.join(basedir, 'kanban.db')}"

# Crear el motor de la base de datos
engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=False)

# Crear la sesión
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    """Obtener una sesión de base de datos"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    """Inicializar la base de datos"""
    Base.metadata.create_all(bind=engine)

def get_session():
    """Obtener una sesión de base de datos"""
    return SessionLocal()