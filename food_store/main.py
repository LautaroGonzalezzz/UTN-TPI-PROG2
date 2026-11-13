"""
Food Store  Sistema de Gestión de Pedidos de Comida (Consola)
Punto de entrada del programa.
"""

import getpass
import sys
from pathlib import Path

# Asegura que el paquete sea importable al ejecutar desde cualquier ubicación
sys.path.insert(0, str(Path(__file__).resolve().parent))

from enums import Rol, Estado, FormaPago
from excepciones import CredencialesInvalidasError, FoodStoreError
from servicios import (
    CategoriaServicio,
    ProductoServicio,
    UsuarioServicio,
    PedidoServicio,
)
from consola.menu import crear_menu


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


def iniciar_sesion(usuario_servicio: UsuarioServicio):
    """Pantalla de inicio de sesión. Máximo 3 intentos."""
    intentos = 0
    max_intentos = 3

    while intentos < max_intentos:
        print("\n" + "=" * 50)
        print("=== FOOD STORE  INICIO DE SESIÓN ===")
        print("=" * 50)
        mail = input("Mail: ").strip()
        try:
            contrasenia = getpass.getpass("Contraseña: ")
        except Exception:
            # Fallback si getpass no está disponible (algunos entornos)
            contrasenia = input("Contraseña: ")

        try:
            usuario = usuario_servicio.autenticar(mail, contrasenia)
            print(f"\nBienvenido/a, {usuario.nombre_completo()} [{usuario.rol}]")
            return usuario
        except CredencialesInvalidasError:
            intentos += 1
            restantes = max_intentos - intentos
            if restantes > 0:
                print(f"   Mail o contraseña incorrectos. Intentos restantes: {restantes}")
            else:
                print("   Mail o contraseña incorrectos.")
                print("Se agotaron los 3 intentos. El programa finalizará.")
                return None
    return None


def main() -> None:
    # Crear servicios (única fuente de verdad de las colecciones)
    categoria_servicio = CategoriaServicio()
    producto_servicio = ProductoServicio(categoria_servicio)
    usuario_servicio = UsuarioServicio()
    pedido_servicio = PedidoServicio(usuario_servicio, producto_servicio)

    # Datos iniciales
    cargar_datos_iniciales(usuario_servicio, categoria_servicio, producto_servicio)

    print("\n*** Food Store  Sistema de Gestión de Pedidos ***")
    print("Datos de acceso inicial:")
    print("  Admin   admin@foodstore.com / admin123")
    print("  Cliente  juan@cliente.com / cliente123")

    while True:
        usuario = iniciar_sesion(usuario_servicio)
        if usuario is None:
            break  # se agotaron los intentos

        # Polimorfismo: el menú se crea según el rol
        menu = crear_menu(
            usuario,
            categoria_servicio,
            producto_servicio,
            usuario_servicio,
            pedido_servicio,
        )
        cerrar_sesion = menu.mostrar()
        if not cerrar_sesion:
            break  # eligió "Salir"


if __name__ == "__main__":
    main()
