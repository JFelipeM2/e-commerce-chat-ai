"""
Servicio de aplicación para el chat con IA
"""

from datetime import datetime, timezone
from .dtos import ChatRequestDTO, ChatResponseDTO, ChatHistoryDTO, ChatMessageDTO
from src.domain.repositories import IProductRepository, IChatRepository
from src.domain.entities import ChatMessage, ChatContext
from src.infrastructure.llm_providers.gemini_service import GeminiService  


class ChatService:
    """
    Servicio que orquesta el flujo completo del chat inteligente:

    1. Obtiene productos del repositorio
    2. Recupera historial de chat
    3. Construye el contexto conversacional
    4. Llama a GeminiService para obtener respuesta
    5. Guarda mensajes en la base de datos
    """

    def __init__(
        self,
        product_repository: IProductRepository,
        chat_repository: IChatRepository,
        gemini_service: GeminiService,
    ) -> None:
        self._product_repository = product_repository
        self._chat_repository = chat_repository
        self._gemini_service = gemini_service

    def process_message(self, request: ChatRequestDTO) -> ChatResponseDTO:
        """
        Procesa un mensaje del usuario y devuelve la respuesta de la IA

        Args:
            request (ChatRequestDTO): Datos del mensaje del usuario

        Returns:
            ChatResponseDTO: Respuesta generada por la IA
        """
        # 1. Obtener productos
        products = self._product_repository.get_all()

        # 2. Recuperar historial reciente
        history = self._chat_repository.get_recent_messages(
            session_id=request.session_id, limit=6
        )
        context = ChatContext(messages=history)

        # 3. Llamar a Gemini
        assistant_message = self._gemini_service.generate_response(
            user_message=request.message,
            products=products,
            chat_context=context,
        )

        now = datetime.now(timezone.utc)

        # 4. Crear entidades de mensaje y guardar
        user_chat = ChatMessage(
            id=None,
            session_id=request.session_id,
            role="user",
            message=request.message,
            timestamp=now,
        )
        assistant_chat = ChatMessage(
            id=None,
            session_id=request.session_id,
            role="assistant",
            message=assistant_message,
            timestamp=now,
        )

        self._chat_repository.save_message(user_chat)
        self._chat_repository.save_message(assistant_chat)

        # 5. Construir DTO de respuesta
        return ChatResponseDTO(
            session_id=request.session_id,
            user_message=request.message,
            assistant_message=assistant_message,
            timestamp=now,
        )

    def get_history(self, session_id: str) -> ChatHistoryDTO:
        """
        Obtiene el historial de mensajes de una sesión especifica
        """
        messages = self._chat_repository.get_recent_messages(
            session_id=session_id, limit=100
        )
        dto_messages = [ChatMessageDTO.model_validate(m) for m in messages]
        return ChatHistoryDTO(session_id=session_id, messages=dto_messages)
