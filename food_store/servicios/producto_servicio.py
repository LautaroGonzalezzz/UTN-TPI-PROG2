from typing import List, Optional

from entidades import Producto, Categoria
from excepciones import EntidadNoEncontradaError
from servicios.categoria_servicio import CategoriaServicio


class ProductoServicio:
    """Gestiona la colección de productos."""

    def __init__(self, categoria_servicio: CategoriaServicio) -> None:
        self.__productos: List[Producto] = []
        self.__categoria_servicio = categoria_servicio

    def listar(
        self,
        solo_activos: bool = True,
        solo_disponibles_con_stock: bool = False,
        id_categoria: Optional[int] = None,
    ) -> List[Producto]:
        resultado: List[Producto] = []
        for p in self.__productos:
            if solo_activos and p.eliminado:
                continue
            if solo_disponibles_con_stock and (not p.disponible or p.stock <= 0):
                continue
            if id_categoria is not None and p.categoria.id != id_categoria:
                continue
            resultado.append(p)
        return resultado

    def buscar_por_id(self, id_producto: int, solo_activos: bool = True) -> Producto:
        for p in self.__productos:
            if p.id == id_producto:
                if solo_activos and p.eliminado:
                    raise EntidadNoEncontradaError(
                        f"Producto con id {id_producto} no encontrado o eliminado"
                    )
                return p
        raise EntidadNoEncontradaError(
            f"Producto con id {id_producto} no encontrado"
        )

    def crear(
        self,
        nombre: str,
        precio: float,
        descripcion: str,
        stock: int,
        imagen: str,
        disponible: bool,
        id_categoria: int,
    ) -> Producto:
        categoria = self.__categoria_servicio.buscar_por_id(id_categoria)
        producto = Producto(
            nombre=nombre,
            precio=precio,
            descripcion=descripcion,
            stock=stock,
            imagen=imagen,
            disponible=disponible,
            categoria=categoria,
        )
        self.__productos.append(producto)
        return producto

    def editar(
        self,
        id_producto: int,
        nombre: Optional[str] = None,
        precio: Optional[float] = None,
        descripcion: Optional[str] = None,
        stock: Optional[int] = None,
        imagen: Optional[str] = None,
        disponible: Optional[bool] = None,
        id_categoria: Optional[int] = None,
    ) -> Producto:
        producto = self.buscar_por_id(id_producto)
        if nombre is not None and nombre.strip():
            producto.nombre = nombre
        if precio is not None:
            producto.precio = precio
        if descripcion is not None and descripcion.strip() != "":
            producto.descripcion = descripcion
        if stock is not None:
            producto.stock = stock
        if imagen is not None:
            producto.imagen = imagen
        if disponible is not None:
            producto.disponible = disponible
        if id_categoria is not None:
            categoria = self.__categoria_servicio.buscar_por_id(id_categoria)
            producto.categoria = categoria
        return producto

    def eliminar(self, id_producto: int) -> None:
        producto = self.buscar_por_id(id_producto)
        producto.eliminado = True

    def todos(self) -> List[Producto]:
        """Devuelve la lista completa (incluye eliminados) para validaciones internas."""
        return list(self.__productos)
