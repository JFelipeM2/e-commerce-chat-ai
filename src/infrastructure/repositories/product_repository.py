"""
Implementación concreta de IProductRepository usando SQLAlchemy
"""

from typing import List, Optional
from sqlalchemy.orm import Session
from src.domain.repositories import IProductRepository
from src.domain.entities import Product
from src.infrastructure.db.models import ProductModel


class SqlAlchemyProductRepository(IProductRepository):
    """
    Repositorio de productos basado en SQLAlchemy
    """

    def __init__(self, db: Session) -> None:
        self._db = db

    def get_all(self) -> List[Product]:
        """Obtiene todos los productos de la base de datos"""
        rows = self._db.query(ProductModel).all()
        return [
            Product(
                id=row.id,
                name=row.name,
                brand=row.brand,
                category=row.category,
                size=row.size,
                color=row.color,
                price=row.price,
                stock=row.stock,
                description=row.description,
            )
            for row in rows
        ]

    def get_by_id(self, product_id: int) -> Optional[Product]:
        """Obtiene un producto por su ID"""
        row = self._db.query(ProductModel).filter(ProductModel.id == product_id).first()
        if not row:
            return None
        return Product(
            id=row.id,
            name=row.name,
            brand=row.brand,
            category=row.category,
            size=row.size,
            color=row.color,
            price=row.price,
            stock=row.stock,
            description=row.description,
        )
