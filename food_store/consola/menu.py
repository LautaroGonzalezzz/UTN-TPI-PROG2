from abc import ABC, abstractmethod

from entidades import Usuario
from servicios import (
    CategoriaServicio,
    ProductoServicio,
    UsuarioServicio,
    PedidoServicio,
)
from enums import Rol


class Menu(ABC):
    """Clase abstracta de menú. Cada rol tiene su subclase."""

    def __init__(
        self,
        usuario: Usuario,
        categoria_servicio: CategoriaServicio,
        producto_servicio: ProductoServicio,
        usuario_servicio: UsuarioServicio,
        pedido_servicio: PedidoServicio,
    ) -> None:
        self._usuario = usuario
        self._categoria_servicio = categoria_servicio
        self._producto_servicio = producto_servicio
        self._usuario_servicio = usuario_servicio
        self._pedido_servicio = pedido_servicio

    @abstractmethod
    def mostrar(self) -> bool:
        """
        Muestra el menú y gestiona las opciones.
        Returns:
            True   cerrar sesión (volver al login)
            False  salir del programa
        """
        ...


def crear_menu(
    usuario: Usuario,
    categoria_servicio: CategoriaServicio,
    producto_servicio: ProductoServicio,
    usuario_servicio: UsuarioServicio,
    pedido_servicio: PedidoServicio,
) -> Menu:
    """Factory: crea el menú según el rol (único punto de decisión por rol)."""
    from consola.menu_administrador import MenuAdministrador
    from consola.menu_cliente import MenuCliente

    if usuario.rol == Rol.ADMIN:
        return MenuAdministrador(
            usuario,
            categoria_servicio,
            producto_servicio,
            usuario_servicio,
            pedido_servicio,
        )
    return MenuCliente(
        usuario,
        categoria_servicio,
        producto_servicio,
        usuario_servicio,
        pedido_servicio,
    )
