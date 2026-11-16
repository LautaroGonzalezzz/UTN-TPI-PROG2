from consola.estilos import aviso, error
from consola.menu import Menu, Opcion
from consola.utilidades import pedir_entero, pedir_si_no
from consola.vistas import (
    mostrar_categorias,
    mostrar_datos_usuario,
    mostrar_detalle_pedido,
    mostrar_pedidos,
    mostrar_productos,
)


class MenuCliente(Menu):
    """Menú de solo consulta para el rol USUARIO."""

    def mostrar(self) -> bool:
        opciones: list[Opcion] = [
            ("1", "Ver categorías", self._ver_categorias),
            ("2", "Ver productos disponibles", self._ver_productos),
            ("3", "Mis pedidos", self._mis_pedidos),
            ("4", "Mis datos", self._mis_datos),
        ]
        titulo: str = f"=== FOOD STORE – CLIENTE ({self._usuario.nombre_completo()}) ==="
        return self._ejecutar_menu_principal(titulo, opciones, pausar=True)

    def _ver_categorias(self) -> None:
        mostrar_categorias(self._categoria_servicio.listar())

    def _ver_productos(self) -> None:
        disponibles = self._producto_servicio.listar(solo_disponibles_con_stock=True)
        mostrar_productos(disponibles, "No hay productos disponibles con stock.")

    def _mis_pedidos(self) -> None:
        pedidos = self._pedido_servicio.listar(id_usuario=self._usuario.id)
        if not pedidos:
            aviso("No tenés pedidos registrados.")
            return
        mostrar_pedidos(pedidos, "", con_usuario=False)

        if not pedir_si_no("¿Ver detalles de algún pedido?"):
            return
        id_pedido: int = pedir_entero("Id del pedido: ", minimo=1)
        pedido = self._pedido_servicio.buscar_por_id(id_pedido)
        if pedido.usuario.id != self._usuario.id:
            error("Pedido no encontrado.")  # un pedido ajeno se informa como inexistente
            return
        mostrar_detalle_pedido(pedido)

    def _mis_datos(self) -> None:
        mostrar_datos_usuario(self._usuario)
