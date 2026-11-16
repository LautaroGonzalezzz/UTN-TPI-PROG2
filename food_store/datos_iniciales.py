"""Datos de ejemplo que se cargan al arrancar (el administrador inicial es obligatorio)."""

from enums import Rol
from servicios import CategoriaServicio, ProductoServicio, UsuarioServicio


def cargar_datos_iniciales(
    usuario_servicio: UsuarioServicio,
    categoria_servicio: CategoriaServicio,
    producto_servicio: ProductoServicio,
) -> None:
    """Carga el administrador inicial y datos de ejemplo."""
    # Administrador obligatorio
    usuario_servicio.crear(
        nombre="Ana",
        apellido="Pérez",
        mail="admin@foodstore.com",
        celular="1111111111",
        contrasenia="admin123",
        rol=Rol.ADMIN,
    )
    # Cliente de ejemplo
    usuario_servicio.crear(
        nombre="Juan",
        apellido="Gómez",
        mail="juan@cliente.com",
        celular="2222222222",
        contrasenia="cliente123",
        rol=Rol.USUARIO,
    )
    # Categorías de ejemplo
    cat1 = categoria_servicio.crear("Pizzas", "Pizzas artesanales y clásicas")
    cat2 = categoria_servicio.crear("Bebidas", "Gaseosas, jugos y agua")
    cat3 = categoria_servicio.crear("Postres", "Dulces y helados")

    # Productos de ejemplo
    producto_servicio.crear(
        "Muzzarella", 8500.0, "Pizza clásica de muzzarella", 20, "muzzarella.jpg", True, cat1.id
    )
    producto_servicio.crear(
        "Napolitana", 9500.0, "Tomate, ajo y orégano", 15, "napolitana.jpg", True, cat1.id
    )
    producto_servicio.crear(
        "Coca-Cola 1.5L", 2500.0, "Gaseosa cola", 50, "coca.jpg", True, cat2.id
    )
    producto_servicio.crear(
        "Agua mineral", 1200.0, "Agua sin gas 500ml", 40, "agua.jpg", True, cat2.id
    )
    producto_servicio.crear(
        "Flan casero", 3000.0, "Flan con dulce de leche", 10, "flan.jpg", True, cat3.id
    )
