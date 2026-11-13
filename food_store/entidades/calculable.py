from abc import ABC, abstractmethod


class Calculable(ABC):
    """Interfaz que define el comportamiento de cálculo de total."""

    @abstractmethod
    def calcular_total(self) -> None:
        """Actualiza el total del objeto que implementa la interfaz."""
        ...
