"""Lectura validada desde teclado. Nunca lanza por entradas mal escritas: vuelve a pedir."""

from enum import Enum
from typing import List, Optional, Type, TypeVar

from consola.estilos import GRIS, error, pintar

E = TypeVar("E", bound=Enum)


def pedir_texto(mensaje: str, obligatorio: bool = True, permitir_vacio: bool = False) -> str:
    """Pide un texto. Si permitir_vacio=True devuelve '' al presionar Enter."""
    while True:
        valor: str = input(mensaje).strip()
        if valor:
            return valor
        if permitir_vacio or not obligatorio:
            return ""
        error("El valor no puede estar vacío. Intente de nuevo.")


def pedir_entero(mensaje: str, minimo: Optional[int] = None, maximo: Optional[int] = None) -> int:
    """Pide un número entero dentro del rango indicado."""
    while True:
        try:
            valor: int = int(input(mensaje).strip())
        except ValueError:
            error("Ingrese un número entero válido.")
            continue
        if minimo is not None and valor < minimo:
            error(f"El valor debe ser >= {minimo}")
        elif maximo is not None and valor > maximo:
            error(f"El valor debe ser <= {maximo}")
        else:
            return valor


def pedir_float(mensaje: str, minimo: Optional[float] = None) -> float:
    """Pide un número decimal (acepta coma o punto)."""
    while True:
        try:
            valor: float = float(input(mensaje).strip().replace(",", "."))
        except ValueError:
            error("Ingrese un número válido.")
            continue
        if minimo is not None and valor < minimo:
            error(f"El valor debe ser >= {minimo}")
        else:
            return valor


def pedir_si_no(mensaje: str) -> bool:
    """Pregunta S/N y devuelve True para sí."""
    while True:
        valor: str = input(f"{mensaje} (S/N): ").strip().upper()
        if valor in ("S", "SI", "SÍ"):
            return True
        if valor in ("N", "NO"):
            return False
        error("Responda S o N.")


def pedir_si_no_opcional(mensaje: str) -> Optional[bool]:
    """S/N; Enter devuelve None (conservar el valor actual)."""
    while True:
        valor: str = input(f"{mensaje} (S/N, Enter = conservar): ").strip().upper()
        if valor == "":
            return None
        if valor in ("S", "SI", "SÍ"):
            return True
        if valor in ("N", "NO"):
            return False
        error("Responda S, N o Enter.")


def pedir_enum(mensaje: str, enum_cls: Type[E]) -> E:
    """Muestra las opciones de un Enum numeradas y pide la elección por número."""
    miembros: List[E] = list(enum_cls)
    print(mensaje)
    for i, miembro in enumerate(miembros, start=1):
        print(f"  {i}. {miembro.value}")
    while True:
        try:
            opcion: int = int(input("Seleccione: ").strip())
        except ValueError:
            error("Ingrese un número válido.")
            continue
        if 1 <= opcion <= len(miembros):
            return miembros[opcion - 1]
        error(f"Opción fuera de rango (1-{len(miembros)})")


def pedir_enum_opcional(mensaje: str, enum_cls: Type[E]) -> Optional[E]:
    """Elige un miembro del Enum por número; Enter devuelve None (conservar)."""
    miembros: List[E] = list(enum_cls)
    print(mensaje)
    for i, miembro in enumerate(miembros, start=1):
        print(f"  {i}. {miembro.value}")
    while True:
        texto: str = input("Seleccione (Enter = conservar): ").strip()
        if texto == "":
            return None
        try:
            opcion: int = int(texto)
        except ValueError:
            error("Ingrese un número válido.")
            continue
        if 1 <= opcion <= len(miembros):
            return miembros[opcion - 1]
        error(f"Opción fuera de rango (1-{len(miembros)})")


def pausa() -> None:
    """Espera Enter para que el usuario alcance a leer el resultado."""
    input(pintar("\nPresione Enter para continuar...", GRIS))
