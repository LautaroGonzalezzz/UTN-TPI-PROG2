from abc import ABC, abstractmethod
from typing import Callable, Sequence

from consola.estilos import (
    GRIS,
    banner,
    error,
    exito,
    info,
    limpiar_pantalla,
    linea,
    pintar,
    titulo,
)
from consola.teclado import elegir_opcion
from consola.utilidades import pausa
from entidades import Usuario
from enums import Rol
from excepciones import FoodStoreError
from servicios import (
    CategoriaServicio,
    PedidoServicio,
    ProductoServicio,
    UsuarioServicio,
)

Accion = Callable[[], None]
Opcion = tuple[str, str, Accion]  # (clave, texto, acción)

CLAVE_CERRAR_SESION: str = "9"
CLAVE_SALIR: str = "0"


class Menu(ABC):
    """Clase abstracta de menú. Cada rol tiene su subclase (polimorfismo)."""

    def __init__(
        self,
        usuario: Usuario,
        categoria_servicio: CategoriaServicio,
        producto_servicio: ProductoServicio,
        usuario_servicio: UsuarioServicio,
        pedido_servicio: PedidoServicio,
    ) -> None:
        self._usuario: Usuario = usuario
        self._categoria_servicio: CategoriaServicio = categoria_servicio
        self._producto_servicio: ProductoServicio = producto_servicio
        self._usuario_servicio: UsuarioServicio = usuario_servicio
        self._pedido_servicio: PedidoServicio = pedido_servicio

    @abstractmethod
    def mostrar(self) -> bool:
        """Muestra el menú y gestiona las opciones.

        Returns:
            True para cerrar sesión (volver al login), False para salir del programa.
        """
        ...

    # ------------------------------------------------------------------
    # Piezas compartidas por todos los menús
    # ------------------------------------------------------------------
    def _cabecera(self, texto: str) -> None:
        """Limpia la pantalla y dibuja banner, barra de sesión y título."""
        limpiar_pantalla()
        banner()
        print(pintar(f" Sesión: {self._usuario.nombre_completo()} · {self._usuario.rol}", GRIS))
        linea()
        titulo(texto)
        print()

    def _ejecutar_accion(self, accion: Accion) -> None:
        """Ejecuta una acción mostrando los errores de negocio sin cerrar el programa."""
        try:
            accion()
        except FoodStoreError as e:
            error(e.mensaje)
        except ValueError:
            error("Valor numérico inválido.")

    def _ejecutar_submenu(self, texto: str, opciones: Sequence[Opcion]) -> None:
        """Bucle genérico de un submenú: ejecuta la acción elegida hasta elegir Volver."""
        visibles: list[tuple[str, str]] = [(c, t) for c, t, _ in opciones] + [("0", "Volver")]
        acciones: dict[str, Accion] = {c: a for c, _, a in opciones}
        while True:
            clave: str = elegir_opcion(visibles, lambda: self._cabecera(texto))
            if clave == "0":
                return
            self._ejecutar_accion(acciones[clave])
            pausa()

    def _ejecutar_menu_principal(
        self,
        texto: str,
        opciones: Sequence[Opcion],
        pausar: bool,
    ) -> bool:
        """Bucle del menú principal. Devuelve True (cerrar sesión) o False (salir)."""
        visibles: list[tuple[str, str]] = (
            [(c, t) for c, t, _ in opciones]
            + [(CLAVE_CERRAR_SESION, "Cerrar sesión"), (CLAVE_SALIR, "Salir")]
        )
        acciones: dict[str, Accion] = {c: a for c, _, a in opciones}
        while True:
            clave: str = elegir_opcion(visibles, lambda: self._cabecera(texto))
            if clave == CLAVE_CERRAR_SESION:
                exito("Sesión cerrada.")
                return True
            if clave == CLAVE_SALIR:
                info("¡Hasta luego!")
                return False
            self._ejecutar_accion(acciones[clave])
            if pausar:
                pausa()


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
            usuario, categoria_servicio, producto_servicio, usuario_servicio, pedido_servicio
        )
    return MenuCliente(
        usuario, categoria_servicio, producto_servicio, usuario_servicio, pedido_servicio
    )
