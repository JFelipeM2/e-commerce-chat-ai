"""
Modulo de entidades de dominio

Aqui se definen las entidades puras del negocio
- Product
- ChatMessage
- ChatContext

No hay dependencias a frameworks ni a la base de datos
"""

from dataclasses import dataclass
from typing import Optional, List
from datetime import datetime


@dataclass
class Product:
    """
    Entidad que representa un producto (zapato) en el e-commerce

    Aplica reglas de negocio basicas:
    - El precio debe ser mayor que 0
    - El stock no puede ser negativo
    - El nombre no puede estar vacío
    """

    id: Optional[int]
    name: str
    brand: str
    category: str
    size: str
    color: str
    price: float
    stock: int
    description: str

    def __post_init__(self) -> None:
        """Realiza validaciones inmediatamente despues de crear el objeto"""
        if not self.name or not self.name.strip():
            raise ValueError("El nombre del producto no puede estar vacio")
        if self.price <= 0:
            raise ValueError("El precio del producto debe ser mayor que 0")
        if self.stock < 0:
            raise ValueError("El stock no puede ser negativo")

    def is_available(self) -> bool:
        """
        Indica si el producto tiene stock disponible

        Returns:
            bool: True si el stock es mayor que cero
        """
        return self.stock > 0

    def reduce_stock(self, quantity: int) -> None:
        """
        Reduce el stock del producto

        Args:
            quantity (int): Cantidad a descontar del stock actual

        Raises:
            ValueError: Si la cantidad no es positiva o no hay suficiente stock
        """
        if quantity <= 0:
            raise ValueError("La cantidad a reducir debe ser positiva")
        if quantity > self.stock:
            raise ValueError("No hay suficiente stock para realizar la operacion")
        self.stock -= quantity

    def increase_stock(self, quantity: int) -> None:
        """
        Aumenta el stock del producto

        Args:
            quantity (int): Cantidad a sumar al stock actual

        Raises:
            ValueError: Si la cantidad no es positiva
        """
        if quantity <= 0:
            raise ValueError("La cantidad a aumentar debe ser positiva")
        self.stock += quantity


@dataclass
class ChatMessage:
    """
    Entidad que representa un mensaje dentro de una conversación de chat

    Attributes:
        id: Identificador opcional en la base de datos
        session_id: Identificador de la sesión del cliente
        role: 'user' o 'assistant'
        mesage: Contenido del mensaje.
        timestamp: Momento en que se generó el mensaje
    """

    id: Optional[int]
    session_id: str
    role: str  # 'user' o 'assistant'
    message: str
    timestamp: datetime

    def __post_init__(self) -> None:
        """Valida los campos inmediatamente despues de crear el objeto"""
        if self.role not in {"user", "assistant"}:
            raise ValueError("role debe ser 'user' o 'assistant'")
        if not self.session_id or not self.session_id.strip():
            raise ValueError("session_id no puede estar vacío")
        if not self.message or not self.message.strip():
            raise ValueError("El mensaje no puede estar vacío")

    def is_from_user(self) -> bool:
        """Retorna True si el mensaje fue enviado por el usuario"""
        return self.role == "user"

    def is_from_assistant(self) -> bool:
        """Retorna True si el mensaje fue enviado por el asistente"""
        return self.role == "assistant"


@dataclass
class ChatContext:
    """
    Value Object que encapsula el contexto de una conversación

    Mantiene los mensajes recientes para dar coherencia al chat
    """

    messages: List[ChatMessage]
    max_messages: int = 6

    def get_recent_messages(self) -> List[ChatMessage]:
        """
        Retorna los últimos N mensajes de la conversación

        Returns:
            list[ChatMessage]: Lista con los mensajes más recientes
        """
        return self.messages[-self.max_messages :]

    def format_for_prompt(self) -> str:
        """
        Formatea los mensajes recientes para incluirlos en el prompt de IA

        Formato:
            Usuario: ...
            Asistente: ...
        """
        lines: list[str] = []
        for msg in self.get_recent_messages():
            prefix = "Usuario" if msg.is_from_user() else "Asistente"
            lines.append(f"{prefix}: {msg.message}")
        return "\n".join(lines)
