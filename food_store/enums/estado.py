from enum import Enum


class Estado(Enum):
    PENDIENTE = "PENDIENTE"
    CONFIRMADO = "CONFIRMADO"
    TERMINADO = "TERMINADO"
    CANCELADO = "CANCELADO"

    def __str__(self) -> str:
        return self.value
