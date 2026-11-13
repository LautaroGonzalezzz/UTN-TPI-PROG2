from typing import List, Optional

from entidades import Categoria, Producto
from excepciones import (
    EntidadNoEncontradaError,
    DuplicadoError,
    OperacionNoPermitidaError,
)


class CategoriaServicio:
    """Gestiona la colección de categorías y las reglas de negocio asociadas."""

    def __init__(self) -> None:
        self.__categorias: List[Categoria] = []

    def listar(self, solo_activos: bool = True) -> List[Categoria]:
        if solo_activos:
            return [c for c in self.__categorias if not c.eliminado]
        return list(self.__categorias)

    def buscar_por_id(self, id_categoria: int, solo_activos: bool = True) -> Categoria:
        for c in self.__categorias:
            if c.id == id_categoria:
                if solo_activos and c.eliminado:
                    raise EntidadNoEncontradaError(
                        f"Categoría con id {id_categoria} no encontrada o eliminada"
                    )
                return c
        raise EntidadNoEncontradaError(
            f"Categoría con id {id_categoria} no encontrada"
        )

    def _existe_nombre(self, nombre: str, excluir_id: Optional[int] = None) -> bool:
        nombre_norm = nombre.strip().lower()
        for c in self.__categorias:
            if c.eliminado:
                continue
            if excluir_id is not None and c.id == excluir_id:
                continue
            if c.nombre.lower() == nombre_norm:
                return True
        return False

    def crear(self, nombre: str, descripcion: str) -> Categoria:
        if self._existe_nombre(nombre):
            raise DuplicadoError(f"Ya existe una categoría con el nombre '{nombre}'")
        categoria = Categoria(nombre, descripcion)
        self.__categorias.append(categoria)
        return categoria

    def editar(
        self,
        id_categoria: int,
        nombre: Optional[str] = None,
        descripcion: Optional[str] = None,
    ) -> Categoria:
        categoria = self.buscar_por_id(id_categoria)
        if nombre is not None and nombre.strip():
            if self._existe_nombre(nombre, excluir_id=id_categoria):
                raise DuplicadoError(f"Ya existe una categoría con el nombre '{nombre}'")
            categoria.nombre = nombre
        if descripcion is not None and descripcion.strip():
            categoria.descripcion = descripcion
        return categoria

    def eliminar(self, id_categoria: int, productos: List[Producto]) -> None:
        categoria = self.buscar_por_id(id_categoria)
        activos = [
            p
            for p in productos
            if not p.eliminado and p.categoria.id == id_categoria
        ]
        if activos:
            raise OperacionNoPermitidaError(
                f"No se puede eliminar la categoría: tiene {len(activos)} producto(s) activo(s)"
            )
        categoria.eliminado = True
