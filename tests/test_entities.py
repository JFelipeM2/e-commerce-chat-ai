"""
Tests basicos para las entidades del dominio
"""

from datetime import datetime
from src.domain.entities import Product, ChatMessage, ChatContext


def test_product_validations():
    product = Product(
        id=1,
        name="Test Shoe",
        brand="Test",
        category="Running",
        size="42",
        color="Negro",
        price=100.0,
        stock=5,
        description="Producto de prueba",
    )
    assert product.is_available()
    product.reduce_stock(2)
    assert product.stock == 3
    product.increase_stock(1)
    assert product.stock == 4


def test_chat_context_format():
    msg1 = ChatMessage(
        id=None,
        session_id="s1",
        role="user",
        message="Hola",
        timestamp=datetime.utcnow(),
    )
    msg2 = ChatMessage(
        id=None,
        session_id="s1",
        role="assistant",
        message="Hola, ¿en que te ayudo?",
        timestamp=datetime.utcnow(),
    )
    ctx = ChatContext(messages=[msg1, msg2])
    formatted = ctx.format_for_prompt()
    assert "Usuario: Hola" in formatted
    assert "Asistente: Hola, ¿en que te ayudo?" in formatted
