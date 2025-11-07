"""
Excepciones especificas del dominio.

Estas excepciones representan errores de negocio, no errores tecnicos
"""


class ProductNotFoundError(Exception):
    """Se lanza cuando no se encuentra un producto solicitado"""

    def __init__(self, product_id: int) -> None:
        super().__init__(f"Producto con id {product_id} no encontrado")
        self.product_id = product_id


class InvalidProductDataError(Exception):
    """Se lanza cuando los datos de un producto son invalidos"""

    def __init__(self, message: str) -> None:
        super().__init__(message)
