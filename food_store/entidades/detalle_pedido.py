from entidades.base import Base
from entidades.producto import Producto
from excepciones import DatoInvalidoError
from formato import formato_pesos


class DetallePedido(Base):
    """Detalle de un pedido. Solo es creado por Pedido (composición)."""

    def __init__(self, cantidad: int, producto: Producto) -> None:
        super().__init__()
        if cantidad <= 0:
            raise DatoInvalidoError("La cantidad debe ser mayor a 0")
        self.__cantidad: int = cantidad
        self.__producto: Producto = producto
        # Precio tomado del producto en el momento de crear el detalle
        self.__subtotal: float = cantidad * producto.precio

    @property
    def cantidad(self) -> int:
        return self.__cantidad

    def sumar_cantidad(self, extra: int) -> None:
        """Suma cantidad a un detalle existente y recalcula subtotal."""
        if extra <= 0:
            raise DatoInvalidoError("La cantidad a sumar debe ser mayor a 0")
        self.__cantidad += extra
        self.__subtotal = self.__cantidad * self.__producto.precio

    @property
    def producto(self) -> Producto:
        return self.__producto

    @property
    def subtotal(self) -> float:
        return self.__subtotal

    def __str__(self) -> str:
        return (
            f"  - {self.producto.nombre} x{self.cantidad} "
            f"({formato_pesos(self.producto.precio)}) = {formato_pesos(self.subtotal)}"
        )
