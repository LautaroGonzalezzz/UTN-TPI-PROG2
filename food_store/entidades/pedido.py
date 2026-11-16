from datetime import date
from typing import List, Optional, Tuple

from entidades.base import Base
from entidades.calculable import Calculable
from entidades.detalle_pedido import DetallePedido
from entidades.producto import Producto
from entidades.usuario import Usuario
from enums import Estado, FormaPago
from formato import formato_fecha, formato_pesos
from excepciones import (
    DatoInvalidoError,
    StockInsuficienteError,
    OperacionNoPermitidaError,
)


class Pedido(Base, Calculable):
    """Pedido de un usuario. Posee composición con DetallePedido."""

    def __init__(self, usuario: Usuario, forma_pago: FormaPago) -> None:
        super().__init__()
        if usuario is None or usuario.eliminado:
            raise DatoInvalidoError("El pedido requiere un usuario activo")
        self.__usuario: Usuario = usuario
        self.__fecha: date = date.today()
        self.__estado: Estado = Estado.PENDIENTE
        self.__total: float = 0.0
        self.__forma_pago: FormaPago = FormaPago.EFECTIVO
        self.forma_pago = forma_pago
        self.__detalles: List[DetallePedido] = []

    @property
    def usuario(self) -> Usuario:
        return self.__usuario

    @property
    def fecha(self) -> date:
        return self.__fecha

    @property
    def estado(self) -> Estado:
        return self.__estado

    @estado.setter
    def estado(self, nuevo: Estado) -> None:
        if not isinstance(nuevo, Estado):
            raise DatoInvalidoError("Estado inválido")
        actual = self.__estado
        # Transiciones válidas
        permitidas: dict[Estado, set[Estado]] = {
            Estado.PENDIENTE: {Estado.CONFIRMADO, Estado.CANCELADO},
            Estado.CONFIRMADO: {Estado.TERMINADO, Estado.CANCELADO},
            Estado.TERMINADO: set(),
            Estado.CANCELADO: set(),
        }
        if nuevo not in permitidas.get(actual, set()):
            raise OperacionNoPermitidaError(
                f"No se puede pasar de {actual} a {nuevo}"
            )
        self.__estado = nuevo

    @property
    def total(self) -> float:
        return self.__total

    @property
    def forma_pago(self) -> FormaPago:
        return self.__forma_pago

    @forma_pago.setter
    def forma_pago(self, valor: FormaPago) -> None:
        if not isinstance(valor, FormaPago):
            raise DatoInvalidoError("Forma de pago inválida")
        self.__forma_pago = valor

    @property
    def detalles(self) -> Tuple[DetallePedido, ...]:
        """Devuelve una tupla (copia inmutable) de los detalles."""
        return tuple(self.__detalles)

    def buscar_detalle_por_producto(self, producto: Producto) -> Optional[DetallePedido]:
        for d in self.__detalles:
            if d.producto.id == producto.id:
                return d
        return None

    def agregar_detalle(self, cantidad: int, producto: Producto) -> None:
        if cantidad <= 0:
            raise DatoInvalidoError("La cantidad debe ser mayor a 0")
        if producto is None or producto.eliminado:
            raise DatoInvalidoError("El producto no existe o está eliminado")
        if not producto.disponible:
            raise DatoInvalidoError("El producto no está disponible")
        if cantidad > producto.stock:
            raise StockInsuficienteError(
                f"Stock insuficiente de '{producto.nombre}'. Disponible: {producto.stock}"
            )

        existente = self.buscar_detalle_por_producto(producto)
        if existente is not None:
            # Verificar stock total que quedaría
            nueva_cantidad = existente.cantidad + cantidad
            if nueva_cantidad > producto.stock:
                raise StockInsuficienteError(
                    f"Stock insuficiente de '{producto.nombre}'. Disponible: {producto.stock}"
                )
            existente.sumar_cantidad(cantidad)
        else:
            detalle = DetallePedido(cantidad, producto)
            self.__detalles.append(detalle)

        self.calcular_total()

    def eliminar_detalle_por_producto(self, producto: Producto) -> None:
        detalle = self.buscar_detalle_por_producto(producto)
        if detalle is None:
            raise DatoInvalidoError("El producto no está en el pedido")
        self.__detalles.remove(detalle)
        self.calcular_total()

    def calcular_total(self) -> None:
        self.__total = sum(d.subtotal for d in self.__detalles)

    def devolver_stock(self) -> None:
        """Devuelve el stock de todos los detalles (al cancelar/eliminar)."""
        for d in self.__detalles:
            d.producto.stock += d.cantidad

    def descontar_stock(self) -> None:
        """Descuenta el stock de todos los detalles (al confirmar creación)."""
        for d in self.__detalles:
            if d.cantidad > d.producto.stock:
                raise StockInsuficienteError(
                    f"Stock insuficiente de '{d.producto.nombre}'"
                )
            d.producto.stock -= d.cantidad

    def __str__(self) -> str:
        return (
            f"[{self.id}] {self.usuario.nombre_completo()} | {self.estado} | "
            f"{self.forma_pago} | Total: {formato_pesos(self.total)} | {formato_fecha(self.fecha)}"
        )
