class FoodStoreError(Exception):
    """Excepción base del sistema Food Store."""

    def __init__(self, mensaje: str) -> None:
        super().__init__(mensaje)
        self.mensaje = mensaje


class EntidadNoEncontradaError(FoodStoreError):
    """Se lanza cuando un id no existe o la entidad está eliminada."""


class DatoInvalidoError(FoodStoreError):
    """Se lanza por datos vacíos, formatos incorrectos o valores fuera de rango."""


class PrecioInvalidoError(DatoInvalidoError):
    """Precio negativo o inválido."""


class StockInsuficienteError(FoodStoreError):
    """Cantidad pedida mayor al stock disponible."""


class DuplicadoError(FoodStoreError):
    """Mail o nombre de categoría ya existente."""


class OperacionNoPermitidaError(FoodStoreError):
    """Transición de estado inválida, categoría con productos, admin que se autoelimina, etc."""


class CredencialesInvalidasError(FoodStoreError):
    """Mail o contraseña incorrectos, o usuario eliminado."""
