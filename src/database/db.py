"""Gestor de base de datos."""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import StaticPool
from config import DATABASE_URL
from src.database.models import Base
from typing import Optional


class GestorBD:
    """Gestor de conexiones y operaciones con la base de datos."""
    
    _instancia = None
    _engine = None
    _SessionLocal = None
    
    def __new__(cls):
        if cls._instancia is None:
            cls._instancia = super(GestorBD, cls).__new__(cls)
            cls._instancia._inicializar()
        return cls._instancia
    
    def _inicializar(self):
        """Inicializa la conexión a la base de datos."""
        # Crear engine
        if "sqlite" in DATABASE_URL:
            self._engine = create_engine(
                DATABASE_URL,
                connect_args={"check_same_thread": False},
                poolclass=StaticPool,
            )
        else:
            self._engine = create_engine(DATABASE_URL, pool_pre_ping=True)
        
        # Crear tablas
        Base.metadata.create_all(bind=self._engine)
        
        # Crear sesión
        self._SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self._engine)
    
    def obtener_sesion(self) -> Session:
        """Obtiene una nueva sesión de base de datos."""
        return self._SessionLocal()
    
    def cerrar_sesion(self, sesion: Session):
        """Cierra una sesión de base de datos."""
        if sesion:
            sesion.close()
    
    def obtener_engine(self):
        """Retorna el engine de SQLAlchemy."""
        return self._engine


def obtener_bd():
    """Función auxiliar para obtener gestor de BD."""
    return GestorBD()
