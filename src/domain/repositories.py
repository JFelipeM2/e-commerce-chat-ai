"""
Interfaces de repositorio del dominio

Definen el contrato para acceder a productos y mensajes de chat sin
depender de una implementación concreta 
"""

from abc import ABC, abstractmethod
from typing import List, Optional
from .entities import Product, ChatMessage


class IProductRepository(ABC):
    """
    Interface que define el contrato para acceder a productos desde el dominio
    Las implementaciones concretas viven en la capa de infraestructura
    """

    @abstractmethod
    def get_all(self) -> List[Product]:
        """Obtiene todos los productos disponibles"""
        raise NotImplementedError

    @abstractmethod
    def get_by_id(self, product_id: int) -> Optional[Product]:
        """Obtiene un producto por su identificador"""
        raise NotImplementedError


class IChatRepository(ABC):
    """
    Interface para acceder y persistir mensajes de chat
    """

    @abstractmethod
    def get_recent_messages(self, session_id: str, limit: int = 6) -> List[ChatMessage]:
        """Obtiene los últimos mensajes de una sesión"""
        raise NotImplementedError

    @abstractmethod
    def save_message(self, message: ChatMessage) -> ChatMessage:
        """Guarda un mensaje nuevo en la conversación"""
        raise NotImplementedError
