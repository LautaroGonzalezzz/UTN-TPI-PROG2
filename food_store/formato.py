"""Funciones de formato compartidas (sin dependencias del resto del proyecto)."""

from datetime import date, datetime


def formato_pesos(valor: float) -> str:
    """Devuelve un monto como pesos argentinos: 8500.5 -> '$8.500,50'."""
    texto: str = f"{valor:,.2f}"
    return "$" + texto.replace(",", "X").replace(".", ",").replace("X", ".")


def formato_fecha(valor: date | datetime) -> str:
    """Devuelve una fecha como dd/mm/aaaa."""
    return valor.strftime("%d/%m/%Y")
