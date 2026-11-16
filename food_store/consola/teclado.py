"""Lectura de teclas y menú con flechas (↑ ↓ Enter, o la tecla del número).

Solo biblioteca estándar: msvcrt en Windows, termios/tty en Linux y macOS.
Si no hay una terminal interactiva se usa el menú numérico clásico.
"""

import os
import sys
from typing import Callable, Sequence

from consola.estilos import (
    CIAN,
    GRIS,
    NEGRITA,
    error,
    es_interactivo,
    pintar,
)

ARRIBA: str = "ARRIBA"
ABAJO: str = "ABAJO"
ENTER: str = "ENTER"


def leer_tecla() -> str:
    """Lee una tecla sin esperar Enter. Devuelve ARRIBA, ABAJO, ENTER o el carácter."""
    if os.name == "nt":
        import msvcrt

        caracter: str = msvcrt.getwch()
        if caracter in ("\x00", "\xe0"):
            return {"H": ARRIBA, "P": ABAJO}.get(msvcrt.getwch(), "")
        if caracter in ("\r", "\n"):
            return ENTER
        if caracter == "\x03":
            raise KeyboardInterrupt
        return caracter

    import select
    import termios
    import tty

    fd: int = sys.stdin.fileno()
    anterior = termios.tcgetattr(fd)
    try:
        tty.setcbreak(fd)
        byte: bytes = os.read(fd, 1)
        if byte == b"\x1b":
            secuencia: bytes = b""
            while select.select([fd], [], [], 0.05)[0] and len(secuencia) < 2:
                secuencia += os.read(fd, 1)
            return {b"[A": ARRIBA, b"[B": ABAJO}.get(secuencia, "")
        if byte in (b"\r", b"\n"):
            return ENTER
        return byte.decode("utf-8", errors="ignore")
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, anterior)


def elegir_opcion(
    opciones: Sequence[tuple[str, str]],
    cabecera: Callable[[], None],
) -> str:
    """Muestra un menú y devuelve la clave de la opción elegida.

    Args:
        opciones: pares (clave, texto), por ejemplo ("1", "Categorías").
        cabecera: función que imprime el encabezado (limpia pantalla, banner, etc.).

    Returns:
        La clave elegida, ya sea con flechas + Enter o pulsando su número.
    """
    claves: list[str] = [clave for clave, _ in opciones]
    if not es_interactivo():
        return _elegir_por_numero(opciones, cabecera, claves)

    indice: int = 0
    while True:
        cabecera()
        for i, (clave, texto) in enumerate(opciones):
            if i == indice:
                print(pintar(f"  ➜ {clave}. {texto}", NEGRITA, CIAN))
            else:
                print(f"    {clave}. {texto}")
        print(pintar("\n ↑↓ mover · Enter elegir · o pulsá el número", GRIS))
        tecla: str = leer_tecla()
        if tecla == ARRIBA:
            indice = (indice - 1) % len(opciones)
        elif tecla == ABAJO:
            indice = (indice + 1) % len(opciones)
        elif tecla == ENTER:
            return claves[indice]
        elif tecla in claves:
            return tecla


def _elegir_por_numero(
    opciones: Sequence[tuple[str, str]],
    cabecera: Callable[[], None],
    claves: list[str],
) -> str:
    """Menú numérico clásico (sin terminal interactiva)."""
    cabecera()
    for clave, texto in opciones:
        print(f"{clave}. {texto}")
    while True:
        elegida: str = input("Seleccione: ").strip()
        if elegida in claves:
            return elegida
        error("Opción inválida.")
