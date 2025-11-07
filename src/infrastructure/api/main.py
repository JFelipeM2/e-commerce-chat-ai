"""
Punto de entrada de la API (FastAPI)

Define los endpoints HTTP y ensambla las dependencias entre capas
"""

from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from src.infrastructure.db.database import engine, Base, get_db
from src.infrastructure.db.init_data import init_db
from src.infrastructure.repositories.product_repository import SqlAlchemyProductRepository
from src.infrastructure.repositories.chat_repository import SqlAlchemyChatRepository
from src.infrastructure.llm_providers.gemini_service import GeminiService
from src.application.product_service import ProductService
from src.application.chat_service import ChatService
from src.application.dtos import (
    ProductDTO,
    ChatRequestDTO,
    ChatResponseDTO,
    ChatHistoryDTO,
)
from src.domain.exceptions import ProductNotFoundError

# Crear tablas y datos iniciales al iniciar la app
Base.metadata.create_all(bind=engine)
init_db()

app = FastAPI(
    title="E-commerce Chat API",
    description="API REST de e-commerce de zapatos con chat inteligente",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_product_service(db: Session = Depends(get_db)) -> ProductService:
    """Crea una instancia de ProductService con su repositorio concreto"""
    repo = SqlAlchemyProductRepository(db)
    return ProductService(product_repository=repo)


def get_chat_service(db: Session = Depends(get_db)) -> ChatService:
    """Crea una instancia de ChatService con sus dependencias"""
    product_repo = SqlAlchemyProductRepository(db)
    chat_repo = SqlAlchemyChatRepository(db)
    gemini = GeminiService()
    return ChatService(
        product_repository=product_repo,
        chat_repository=chat_repo,
        gemini_service=gemini,
    )


@app.get("/health", tags=["Health"])
def health_check() -> dict:
    """Endpoint simple para verificar que la API esta viva"""
    return {"status": "ok"}


@app.get("/products", response_model=list[ProductDTO], tags=["Productos"])
def list_products(service: ProductService = Depends(get_product_service)):
    """Lista todos los productos del catalogo."""
    return service.list_products()


@app.get(
    "/products/{product_id}",
    response_model=ProductDTO,
    tags=["Productos"],
)
def get_product(
    product_id: int,
    service: ProductService = Depends(get_product_service),
):
    """Obtiene los detalles de un producto especifico."""
    try:
        return service.get_product(product_id)
    except ProductNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc))


@app.post("/chat", response_model=ChatResponseDTO, tags=["Chat"])
def chat(
    request: ChatRequestDTO,
    service: ChatService = Depends(get_chat_service),
):
    """Procesa un mensaje de chat y devuelve la respuesta de la IA"""
    return service.process_message(request)


@app.get(
    "/chat/history/{session_id}",
    response_model=ChatHistoryDTO,
    tags=["Chat"],
)
def chat_history(
    session_id: str,
    service: ChatService = Depends(get_chat_service),
):
    """Obtiene el historial de conversación de una sesión"""
    return service.get_history(session_id)
