"""Estilos de terminal: colores ANSI, banner, mensajes y tablas.

Usa solo la biblioteca estándar. Si la salida no es una terminal (o está
definida la variable NO_COLOR) se imprime texto plano sin secuencias ANSI.
"""

import os
import sys
from typing import Callable, Sequence

from enums import Estado

ANCHO_BANNER: int = 44
ANCHO_LINEA: int = 60
MAX_ANCHO_COLUMNA: int = 32

RESET: str = "\033[0m"
NEGRITA: str = "\033[1m"
ROJO: str = "\033[31m"
VERDE: str = "\033[32m"
AMARILLO: str = "\033[33m"
CIAN: str = "\033[36m"
GRIS: str = "\033[90m"


def _preparar_terminal() -> None:
    """Activa ANSI en Windows y evita errores si la consola no soporta algún símbolo."""
    if os.name == "nt":
        os.system("")  # habilita el procesamiento de secuencias ANSI (Windows 10+)
    reconfigurar = getattr(sys.stdout, "reconfigure", None)
    if reconfigurar is not None:
        reconfigurar(errors="replace")


_preparar_terminal()


def soporta_color() -> bool:
    """True si hay que usar colores (salida en terminal y sin NO_COLOR)."""
    return sys.stdout.isatty() and "NO_COLOR" not in os.environ


def es_interactivo() -> bool:
    """True si hay teclado y pantalla reales (permite el menú con flechas)."""
    return sys.stdin.isatty() and sys.stdout.isatty()


def pintar(texto: str, *estilos: str) -> str:
    """Envuelve el texto con los estilos ANSI indicados (si se soportan)."""
    if not estilos or not soporta_color():
        return texto
    return "".join(estilos) + texto + RESET


def limpiar_pantalla() -> None:
    """Borra la pantalla (solo en terminales reales)."""
    if soporta_color():
        print("\033[2J\033[H", end="")


def exito(mensaje: str) -> None:
    print(pintar(f"   ✔ {mensaje}", VERDE))


def error(mensaje: str) -> None:
    print(pintar(f"   ✖ {mensaje}", ROJO))


def info(mensaje: str) -> None:
    print(pintar(f"   ℹ {mensaje}", CIAN))


def aviso(mensaje: str) -> None:
    print(pintar(f"   ⚠ {mensaje}", AMARILLO))


def linea() -> None:
    print(pintar("─" * ANCHO_LINEA, GRIS))


def titulo(texto: str) -> None:
    """Imprime un título de sección."""
    print(pintar(texto, NEGRITA, CIAN))


def banner(subtitulo: str = "Sistema de Gestión de Pedidos") -> None:
    """Imprime el encabezado de la aplicación dentro de un recuadro."""
    borde_sup: str = "╔" + "═" * ANCHO_BANNER + "╗"
    borde_inf: str = "╚" + "═" * ANCHO_BANNER + "╝"
    lateral: str = pintar("║", CIAN)
    print(pintar(borde_sup, CIAN))
    print(lateral + pintar("F O O D   S T O R E".center(ANCHO_BANNER), NEGRITA) + lateral)
    print(lateral + subtitulo.center(ANCHO_BANNER) + lateral)
    print(pintar(borde_inf, CIAN))


def estilo_estado(texto: str) -> str:
    """Devuelve el color asociado a un estado de pedido (para las tablas)."""
    colores: dict[str, str] = {
        Estado.PENDIENTE.value: AMARILLO,
        Estado.CONFIRMADO.value: CIAN,
        Estado.TERMINADO.value: VERDE,
        Estado.CANCELADO.value: ROJO,
    }
    return colores.get(texto, "")


def _recortar(texto: str) -> str:
    if len(texto) <= MAX_ANCHO_COLUMNA:
        return texto
    return texto[: MAX_ANCHO_COLUMNA - 1] + "…"


def tabla(
    encabezados: Sequence[str],
    filas: Sequence[Sequence[str]],
    alineacion: str = "",
    estilos: dict[int, Callable[[str], str]] | None = None,
) -> None:
    """Imprime una tabla con bordes.

    Args:
        encabezados: títulos de las columnas.
        filas: contenido de cada fila (todo como texto).
        alineacion: una letra por columna, 'l' izquierda o 'r' derecha.
        estilos: por índice de columna, función que recibe el texto de la
            celda y devuelve el código ANSI con que pintarla ('' = sin color).
    """
    columnas: int = len(encabezados)
    aligns: str = alineacion.ljust(columnas, "l")
    datos: list[list[str]] = [[_recortar(c) for c in fila] for fila in filas]
    anchos: list[int] = [
        max([len(encabezados[i])] + [len(fila[i]) for fila in datos])
        for i in range(columnas)
    ]

    def borde(izq: str, medio: str, der: str) -> str:
        return pintar(izq + medio.join("─" * (a + 2) for a in anchos) + der, GRIS)

    def celda(texto: str, i: int, estilo: str = "") -> str:
        relleno: str = texto.rjust(anchos[i]) if aligns[i] == "r" else texto.ljust(anchos[i])
        return " " + (pintar(relleno, estilo) if estilo else relleno) + " "

    barra: str = pintar("│", GRIS)
    print(borde("┌", "┬", "┐"))
    print(barra + barra.join(celda(h, i, NEGRITA) for i, h in enumerate(encabezados)) + barra)
    print(borde("├", "┼", "┤"))
    for fila in datos:
        celdas: list[str] = []
        for i, texto in enumerate(fila):
            funcion = (estilos or {}).get(i)
            celdas.append(celda(texto, i, funcion(texto) if funcion else ""))
        print(barra + barra.join(celdas) + barra)
    print(borde("└", "┴", "┘"))
