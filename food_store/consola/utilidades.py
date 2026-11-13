from typing import Optional, TypeVar, Type, List
from enum import Enum

from excepciones import DatoInvalidoError

E = TypeVar("E", bound=Enum)


def pedir_texto(mensaje: str, obligatorio: bool = True, permitir_vacio: bool = False) -> str:
    """Pide un texto. Si permitir_vacio=True devuelve '' al presionar Enter."""
    while True:
        valor = input(mensaje).strip()
        if valor:
            return valor
        if permitir_vacio or not obligatorio:
            return ""
        print("   El valor no puede estar vacío. Intente de nuevo.")


def pedir_entero(mensaje: str, minimo: Optional[int] = None, maximo: Optional[int] = None) -> int:
    while True:
        try:
            valor = int(input(mensaje).strip())
            if minimo is not None and valor < minimo:
                print(f"   El valor debe ser >= {minimo}")
                continue
            if maximo is not None and valor > maximo:
                print(f"   El valor debe ser <= {maximo}")
                continue
            return valor
        except ValueError:
            print("   Ingrese un número entero válido.")


def pedir_float(mensaje: str, minimo: Optional[float] = None) -> float:
    while True:
        try:
            valor = float(input(mensaje).strip().replace(",", "."))
            if minimo is not None and valor < minimo:
                print(f"   El valor debe ser >= {minimo}")
                continue
            return valor
        except ValueError:
            print("   Ingrese un número válido.")


def pedir_si_no(mensaje: str) -> bool:
    while True:
        valor = input(f"{mensaje} (S/N): ").strip().upper()
        if valor in ("S", "SI", "SÍ"):
            return True
        if valor in ("N", "NO"):
            return False
        print("   Responda S o N.")


def pedir_enum(mensaje: str, enum_cls: Type[E]) -> E:
    """Muestra las opciones de un Enum numeradas y pide la elección."""
    miembros: List[E] = list(enum_cls)
    print(mensaje)
    for i, m in enumerate(miembros, start=1):
        print(f"  {i}. {m.value}")
    while True:
        try:
            opcion = int(input("Seleccione: ").strip())
            if 1 <= opcion <= len(miembros):
                return miembros[opcion - 1]
            print(f"   Opción fuera de rango (1-{len(miembros)})")
        except ValueError:
            print("   Ingrese un número válido.")


def pedir_opcion(mensaje: str, opciones_validas: List[str]) -> str:
    while True:
        valor = input(mensaje).strip()
        if valor in opciones_validas:
            return valor
        print(f"   Opción inválida. Elija entre: {', '.join(opciones_validas)}")


def pausa() -> None:
    input("\nPresione Enter para continuar...")
