from typing import List, Optional

from entidades import Pedido, Producto, Usuario
from enums import Estado, FormaPago
from excepciones import (
    EntidadNoEncontradaError,
    DatoInvalidoError,
    StockInsuficienteError,
)
from servicios.usuario_servicio import UsuarioServicio
from servicios.producto_servicio import ProductoServicio


class PedidoServicio:
    """Gestiona pedidos y sus detalles (composición)."""

    def __init__(
        self,
        usuario_servicio: UsuarioServicio,
        producto_servicio: ProductoServicio,
    ) -> None:
        self.__pedidos: List[Pedido] = []
        self.__usuario_servicio = usuario_servicio
        self.__producto_servicio = producto_servicio

    def listar(
        self,
        solo_activos: bool = True,
        id_usuario: Optional[int] = None,
    ) -> List[Pedido]:
        resultado: List[Pedido] = []
        for p in self.__pedidos:
            if solo_activos and p.eliminado:
                continue
            if id_usuario is not None and p.usuario.id != id_usuario:
                continue
            resultado.append(p)
        return resultado

    def buscar_por_id(self, id_pedido: int, solo_activos: bool = True) -> Pedido:
        for p in self.__pedidos:
            if p.id == id_pedido:
                if solo_activos and p.eliminado:
                    raise EntidadNoEncontradaError(
                        f"Pedido con id {id_pedido} no encontrado o eliminado"
                    )
                return p
        raise EntidadNoEncontradaError(
            f"Pedido con id {id_pedido} no encontrado"
        )

    def crear(
        self,
        id_usuario: int,
        forma_pago: FormaPago,
        items: List[tuple[int, int]],  # [(id_producto, cantidad), ...]
    ) -> Pedido:
        """
        Crea un pedido completo. Si falla cualquier detalle, no se agrega nada
        y no se modifica stock.
        """
        usuario = self.__usuario_servicio.buscar_por_id(id_usuario)
        pedido = Pedido(usuario, forma_pago)

        try:
            for id_prod, cantidad in items:
                producto = self.__producto_servicio.buscar_por_id(id_prod)
                pedido.agregar_detalle(cantidad, producto)
            if not pedido.detalles:
                raise DatoInvalidoError("El pedido debe tener al menos un detalle")
            # Solo si todo está bien se descuenta stock y se guarda
            pedido.descontar_stock()
            self.__pedidos.append(pedido)
            return pedido
        except (StockInsuficienteError, DatoInvalidoError, EntidadNoEncontradaError):
            # No se agregó a la colección ni se descontó stock
            raise

    def cambiar_estado(self, id_pedido: int, nuevo_estado: Estado) -> Pedido:
        pedido = self.buscar_por_id(id_pedido)
        estado_anterior = pedido.estado
        pedido.estado = nuevo_estado  # valida transición
        if nuevo_estado == Estado.CANCELADO and estado_anterior != Estado.CANCELADO:
            pedido.devolver_stock()
        return pedido

    def cambiar_forma_pago(self, id_pedido: int, forma_pago: FormaPago) -> Pedido:
        pedido = self.buscar_por_id(id_pedido)
        pedido.forma_pago = forma_pago
        return pedido

    def eliminar(self, id_pedido: int) -> None:
        pedido = self.buscar_por_id(id_pedido)
        if pedido.estado not in (Estado.TERMINADO, Estado.CANCELADO):
            pedido.devolver_stock()
        pedido.eliminado = True
        for d in pedido.detalles:
            d.eliminado = True
