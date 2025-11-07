"""
Carga de configuración desde variables de entorno

Usa python-dotenv para leer el archivo .env en desarrollo
"""

from functools import lru_cache
from pydantic import BaseModel
from dotenv import load_dotenv
import os

load_dotenv()  # Carga variables desde .env si existe


class Settings(BaseModel):
    """Configuración principal de la aplicación"""

    gemini_api_key: str
    database_url: str
    environment: str = "development"

    class Config:
        frozen = True


@lru_cache
def get_settings() -> Settings:
    """
    Retorna una instancia única (cacheada) de Settings
    """
    return Settings(
        gemini_api_key=os.environ.get("GEMINI_API_KEY", ""),
        database_url=os.environ.get("DATABASE_URL", "sqlite:///./data/ecommerce_chat.db"),
        environment=os.environ.get("ENVIRONMENT", "development"),
    )
