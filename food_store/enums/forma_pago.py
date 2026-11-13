from enum import Enum


class FormaPago(Enum):
    TARJETA = "TARJETA"
    TRANSFERENCIA = "TRANSFERENCIA"
    EFECTIVO = "EFECTIVO"

    def __str__(self) -> str:
        return self.value
