"""
Integración con Google Gemini AI

Este modulo se encarga de construir el prompt y llamar a la API de Gemini
"""

from typing import List
from src.domain.entities import Product, ChatContext
from src.config import get_settings
import google.generativeai as genai


class GeminiService:
    """
    Servicio que encapsula la comunicación con Google Gemini

    Se puede reemplazar por otro proveedor de IA sin afectar el dominio
    ni la capa de aplicación.
    """

    def __init__(self) -> None:
        settings = get_settings()
        genai.configure(api_key=settings.gemini_api_key)
        # Puedes cambiar el modelo si tu profe indicó otro
        self._model = genai.GenerativeModel("gemini-1.5-flash")

    def generate_response(
        self,
        user_message: str,
        products: List[Product],
        chat_context: ChatContext,
    ) -> str:
        """
        Genera una respuesta usando Gemini a partir del mensaje del usuario,
        los productos disponibles y el contexto conversacional.

        Returns:
            str: Texto de respuesta del asistente.
        """
        products_text = "\n".join(
            f"- {p.name} | Marca: {p.brand} | Categoría: {p.category} | "
            f"Talla: {p.size} | Color: {p.color} | Precio: {p.price} | Stock: {p.stock}"
            for p in products
        )

        history_text = chat_context.format_for_prompt()

        prompt = f"""
Eres un asistente de ventas para una tienda de zapatos

Catálogo de productos:
{products_text}

Historial reciente de la conversación:
{history_text}

Mensaje actual del usuario:
Usuario: {user_message}

Responde en un tono amable, profesional y conciso. 
Solo recomienda productos del catálogo disponible.
"""

        result = self._model.generate_content(prompt)
        return result.text.strip()
