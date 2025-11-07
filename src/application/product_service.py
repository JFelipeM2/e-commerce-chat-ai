"""
Servicio de aplicación para casos de uso relacionados con productos
"""

from typing import List
from datetime import datetime
from .dtos import ProductDTO
from src.domain.repositories import IProductRepository
from src.domain.exceptions import ProductNotFoundError


class ProductService:
    """
    Servicio que orquesta las operaciones de negocio sobre productos

    Depende de una implementación de IProductRepository inyectada desde
    la capa de infraestructura
    """

    def __init__(self, product_repository: IProductRepository) -> None:
        self._product_repository = product_repository

    def list_products(self) -> List[ProductDTO]:
        """
        Retorna todos los productos del catalogo

        Returns:
            list[ProductDTO]: Lista de productos disponibles
        """
        products = self._product_repository.get_all()
        return [ProductDTO.model_validate(p) for p in products]

    def get_product(self, product_id: int) -> ProductDTO:
        """
        Obtiene un producto por su ID

        Raises:
            ProductNotFoundError: Si el producto no existe
        """
        product = self._product_repository.get_by_id(product_id)
        if not product:
            raise ProductNotFoundError(product_id)
        return ProductDTO.model_validate(product)
