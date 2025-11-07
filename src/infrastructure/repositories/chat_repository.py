"""
Implementación concreta de IChatRepository usando SQLAlchemy
"""

from typing import List
from sqlalchemy.orm import Session
from datetime import datetime, timezone
from src.domain.repositories import IChatRepository
from src.domain.entities import ChatMessage
from src.infrastructure.db.models import ChatMessageModel


class SqlAlchemyChatRepository(IChatRepository):
    """
    Repositorio de mensajes de chat basado en SQLAlchemy
    """

    def __init__(self, db: Session) -> None:
        self._db = db

    def get_recent_messages(self, session_id: str, limit: int = 6) -> List[ChatMessage]:
        """Obtiene los ultimos N mensajes de una sesión"""
        rows = (
            self._db.query(ChatMessageModel)
            .filter(ChatMessageModel.session_id == session_id)
            .order_by(ChatMessageModel.timestamp.asc())
            .all()
        )
        rows = rows[-limit:]
        return [
            ChatMessage(
                id=row.id,
                session_id=row.session_id,
                role=row.role,
                message=row.message,
                timestamp=row.timestamp,
            )
            for row in rows
        ]

    def save_message(self, message: ChatMessage) -> ChatMessage:
        """Persiste un mensaje de chat en la base de datos"""
        row = ChatMessageModel(
            session_id=message.session_id,
            role=message.role,
            message=message.message,
            timestamp=message.timestamp or datetime.now(timezone.utc),
        )
        self._db.add(row)
        self._db.commit()
        self._db.refresh(row)
        message.id = row.id
        return message
