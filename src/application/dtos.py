"""
DTOs (Data Transfer Objects) usados para comunicar capas

Se basan en Pydantic para validación automática
"""

from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field


class ProductDTO(BaseModel):
    """DTO para exponer datos de productos hacia la API"""

    model_config = ConfigDict(from_attributes=True)

    id: Optional[int] = None
    name: str = Field(..., description="Nombre del zapato")
    brand: str
    category: str
    size: str
    color: str
    price: float = Field(..., gt=0, description="Precio del producto")
    stock: int = Field(..., ge=0, description="Unidades disponibles")
    description: str


class ChatMessageDTO(BaseModel):
    """DTO para mensajes individuales de chat"""

    model_config = ConfigDict(from_attributes=True)

    id: Optional[int] = None
    session_id: str
    role: str
    message: str
    timestamp: datetime


class ChatRequestDTO(BaseModel):
    """DTO de entrada para el endpoint de chat"""

    session_id: str
    message: str


class ChatResponseDTO(BaseModel):
    """DTO de salida para el endpoint de chat"""

    session_id: str
    user_message: str
    assistant_message: str
    timestamp: datetime


class ChatHistoryDTO(BaseModel):
    """DTO para retornar el historial completo de una sesión"""

    session_id: str
    messages: List[ChatMessageDTO]
