from entidades.base import Base
from entidades.categoria import Categoria
from excepciones import DatoInvalidoError, PrecioInvalidoError
from formato import formato_pesos


class Producto(Base):
    """Representa un producto del catálogo."""

    def __init__(
        self,
        nombre: str,
        precio: float,
        descripcion: str,
        stock: int,
        imagen: str,
        disponible: bool,
        categoria: Categoria,
    ) -> None:
        super().__init__()
        self.nombre = nombre
        self.precio = precio
        self.descripcion = descripcion
        self.stock = stock
        self.imagen = imagen
        self.disponible = disponible
        self.categoria = categoria

    @property
    def nombre(self) -> str:
        return self.__nombre

    @nombre.setter
    def nombre(self, valor: str) -> None:
        if not valor or not valor.strip():
            raise DatoInvalidoError("El nombre del producto no puede estar vacío")
        self.__nombre = valor.strip()

    @property
    def precio(self) -> float:
        return self.__precio

    @precio.setter
    def precio(self, valor: float) -> None:
        if valor < 0:
            raise PrecioInvalidoError("El precio no puede ser negativo")
        self.__precio = float(valor)

    @property
    def descripcion(self) -> str:
        return self.__descripcion

    @descripcion.setter
    def descripcion(self, valor: str) -> None:
        if valor is None:
            raise DatoInvalidoError("La descripción no puede ser nula")
        self.__descripcion = valor.strip() if isinstance(valor, str) else str(valor)

    @property
    def stock(self) -> int:
        return self.__stock

    @stock.setter
    def stock(self, valor: int) -> None:
        if valor < 0:
            raise DatoInvalidoError("El stock no puede ser negativo")
        self.__stock = int(valor)

    @property
    def imagen(self) -> str:
        return self.__imagen

    @imagen.setter
    def imagen(self, valor: str) -> None:
        self.__imagen = valor.strip() if valor else ""

    @property
    def disponible(self) -> bool:
        return self.__disponible

    @disponible.setter
    def disponible(self, valor: bool) -> None:
        self.__disponible = bool(valor)

    @property
    def categoria(self) -> Categoria:
        return self.__categoria

    @categoria.setter
    def categoria(self, valor: Categoria) -> None:
        if valor is None or valor.eliminado:
            raise DatoInvalidoError("La categoría debe existir y no estar eliminada")
        self.__categoria = valor

    def _restaurar_categoria(self, categoria: Categoria) -> None:
        """Uso interno de los servicios para deshacer una edición fallida."""
        self.__categoria = categoria

    def __str__(self) -> str:
        disp = "Sí" if self.disponible else "No"
        return (
            f"[{self.id}] {self.nombre} | {formato_pesos(self.precio)} | Stock: {self.stock} | "
            f"Cat: {self.categoria.nombre} | Disp: {disp}"
        )
