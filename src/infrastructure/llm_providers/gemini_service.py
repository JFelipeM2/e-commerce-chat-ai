"""
Integración con Google Gemini AI.

Este módulo se encarga de construir el prompt y llamar a la API de Gemini.
Si la llamada falla (por ejemplo, modelo no disponible o error de clave),
se devuelve una respuesta generada localmente como fallback
"""

from typing import List
from src.domain.entities import Product, ChatContext
from src.config import get_settings
import google.generativeai as genai


class GeminiService:
    """
    Servicio que encapsula la comunicación con Google Gemini.

    Se puede reemplazar por otro proveedor de IA sin afectar el dominio
    ni la capa de aplicación
    """

    def __init__(self) -> None:
        """
        Inicializa la configuración del cliente de Gemini

        Lee la API key desde la configuración y prepara el modelo
        Si hubiera algún problema al crear el modelo, se mantiene en None
        y se usará siempre el modo de fallback
        """
        settings = get_settings()
        genai.configure(api_key=settings.gemini_api_key)

        try:
            self._model = genai.GenerativeModel("gemini-1.5-flash")
        except Exception as e:
            print(f"[GeminiService] Error al inicializar el modelo: {e!r}")
            self._model = None

    def generate_response(
        self,
        user_message: str,
        products: List[Product],
        chat_context: ChatContext,
    ) -> str:
        """
        Genera una respuesta usando Gemini a partir del mensaje del usuario,
        los productos disponibles y el contexto conversacional

        Si ocurre cualquier error al llamar a la API de Gemini, se devuelve
        una respuesta generada localmente como fallback

        Args:
            user_message (str): Mensaje enviado por el usuario
            products (list[Product]): Lista de productos disponibles
            chat_context (ChatContext): Contexto reciente del chat

        Returns:
            str: Texto de respuesta del asistente
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

Responde en un tono amable, profesional y conciso
Solo recomienda productos del catálogo disponible
"""

        # Intentar usar Gemini
        try:
            if self._model is None:
                raise RuntimeError("Modelo de Gemini no inicializado.")

            result = self._model.generate_content(prompt)
            text = getattr(result, "text", "").strip()

            if text:
                return text

            raise RuntimeError("Respuesta vacía desde Gemini.")

        except Exception as e:
            print(f"[GeminiService] Error al generar respuesta con Gemini: {e!r}")
            return self._build_fallback_response(user_message, products, chat_context)

    def _build_fallback_response(
        self,
        user_message: str,
        products: List[Product],
        chat_context: ChatContext,
    ) -> str:
        """
        Genera una respuesta simple usando únicamente la información local

        Este metodo se utiliza cuando la API de Gemini no está disponible
        o produce algun error
        """
        if not products:
            return (
                "En este momento no puedo acceder al servicio de IA, "
                "pero actualmente no hay productos registrados en el catalogo. "
                "Intenta de nuevo mas tarde"
            )

        sample = products[:3]
        recomendaciones = "\n".join(
            f"- {p.name} ({p.brand}) - {p.category}, talla {p.size}, color {p.color}, ${p.price}"
            for p in sample
        )

        return (
            "En este momento tuve un problema al conectarme con el servicio de IA, "
            "pero puedo recomendarte algunas opciones basadas en nuestro catalogo local:\n\n"
            f"{recomendaciones}\n\n"
            "Si necesitas algo mas especifico (talla, color o tipo de zapato), "
            "indicame y tratare de ayudarte con la informacion disponible"
        )
