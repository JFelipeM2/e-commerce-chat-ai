"""
Script para poblar la base de datos con productos de ejemplo
"""

from sqlalchemy.orm import Session
from .database import engine
from .models import Base, ProductModel


def init_db() -> None:
    """
    Crea las tablas y carga algunos productos de ejemplo si la tabla está vacía
    """
    Base.metadata.create_all(bind=engine)
    db = Session(bind=engine)

    if db.query(ProductModel).count() == 0:
        sample_products = [
            ProductModel(
                name="Nike Air Zoom Pegasus",
                brand="Nike",
                category="Running",
                size="42",
                color="Negro",
                price=120.0,
                stock=5,
                description="Las valijas usan nike",
            ),
            ProductModel(
                name="Adidas Ultraboost 21",
                brand="Adidas",
                category="Running",
                size="41",
                color="Blanco",
                price=150.0,
                stock=3,
                description="Alta amortiguación y comodidad para corredores exigentes",
            ),
            ProductModel(
                name="Puma Suede Classic",
                brand="Puma",
                category="Casual",
                size="40",
                color="Azul",
                price=80.0,
                stock=10,
                description="Clasico modelo casual para uso diario",
            ),
        ]
        db.add_all(sample_products)
        db.commit()

    db.close()


if __name__ == "__main__":
    init_db()
