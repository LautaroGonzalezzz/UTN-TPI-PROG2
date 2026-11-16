"""Cómo se muestran las entidades en pantalla (tablas y fichas). Sin reglas de negocio."""

from typing import Sequence

from consola.estilos import (
    AMARILLO,
    CIAN,
    NEGRITA,
    ROJO,
    VERDE,
    aviso,
    estilo_estado,
    pintar,
    tabla,
)
from entidades import Categoria, Pedido, Producto, Usuario
from enums import Rol
from formato import formato_fecha, formato_pesos

STOCK_BAJO: int = 5


def _estilo_stock(texto: str) -> str:
    cantidad: int = int(texto)
    if cantidad == 0:
        return ROJO
    return AMARILLO if cantidad <= STOCK_BAJO else ""


def _estilo_si_no(texto: str) -> str:
    return VERDE if texto == "Sí" else ROJO


def _estilo_rol(texto: str) -> str:
    return CIAN if texto == Rol.ADMIN.value else ""


def mostrar_categorias(categorias: Sequence[Categoria]) -> None:
    if not categorias:
        aviso("No hay categorías cargadas.")
        return
    tabla(
        ["ID", "Nombre", "Descripción"],
        [[str(c.id), c.nombre, c.descripcion] for c in categorias],
        "rll",
    )


def mostrar_productos(productos: Sequence[Producto], mensaje_vacio: str) -> None:
    if not productos:
        aviso(mensaje_vacio)
        return
    tabla(
        ["ID", "Producto", "Precio", "Stock", "Categoría", "Disp."],
        [
            [
                str(p.id),
                p.nombre,
                formato_pesos(p.precio),
                str(p.stock),
                p.categoria.nombre,
                "Sí" if p.disponible else "No",
            ]
            for p in productos
        ],
        "rlrrll",
        {3: _estilo_stock, 5: _estilo_si_no},
    )


def mostrar_usuarios(usuarios: Sequence[Usuario]) -> None:
    if not usuarios:
        aviso("No hay usuarios cargados.")
        return
    tabla(
        ["ID", "Nombre", "Apellido", "Mail", "Rol"],
        [[str(u.id), u.nombre, u.apellido, u.mail, u.rol.value] for u in usuarios],
        "rllll",
        {4: _estilo_rol},
    )


def mostrar_pedidos(pedidos: Sequence[Pedido], mensaje_vacio: str, con_usuario: bool = True) -> None:
    if not pedidos:
        aviso(mensaje_vacio)
        return
    encabezados: list[str] = ["ID"] + (["Cliente"] if con_usuario else []) + [
        "Estado", "Pago", "Total", "Fecha",
    ]
    filas: list[list[str]] = []
    for p in pedidos:
        fila: list[str] = [str(p.id)]
        if con_usuario:
            fila.append(p.usuario.nombre_completo())
        fila += [p.estado.value, p.forma_pago.value, formato_pesos(p.total), formato_fecha(p.fecha)]
        filas.append(fila)
    posicion_estado: int = 2 if con_usuario else 1
    alineacion: str = "r" + ("l" if con_usuario else "") + "llrl"
    tabla(encabezados, filas, alineacion, {posicion_estado: estilo_estado})


def mostrar_detalle_pedido(pedido: Pedido) -> None:
    print(f"\n{pintar(str(pedido), NEGRITA)}")
    if not pedido.detalles:
        aviso("El pedido no tiene detalles.")
        return
    tabla(
        ["Producto", "Cantidad", "Precio", "Subtotal"],
        [
            [d.producto.nombre, str(d.cantidad), formato_pesos(d.producto.precio), formato_pesos(d.subtotal)]
            for d in pedido.detalles
        ],
        "lrrr",
    )
    print(pintar(f"  TOTAL: {formato_pesos(pedido.total)}", NEGRITA, VERDE))


def mostrar_datos_usuario(usuario: Usuario) -> None:
    print()
    for etiqueta, valor in (
        ("Nombre", usuario.nombre),
        ("Apellido", usuario.apellido),
        ("Mail", usuario.mail),
        ("Celular", usuario.celular),
        ("Rol", usuario.rol.value),
    ):
        print(f"  {pintar(etiqueta.ljust(9), NEGRITA)} {valor}")
