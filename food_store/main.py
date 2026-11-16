"""
Food Store – Sistema de Gestión de Pedidos de Comida (Consola)
Punto de entrada del programa.
"""

import sys
from pathlib import Path

# Asegura que el paquete sea importable al ejecutar desde cualquier ubicación
sys.path.insert(0, str(Path(__file__).resolve().parent))

from consola.menu import crear_menu
from consola.sesion import iniciar_sesion
from datos_iniciales import cargar_datos_iniciales
from servicios import (
    CategoriaServicio,
    PedidoServicio,
    ProductoServicio,
    UsuarioServicio,
)




def main() -> None:
    """Crea los servicios, carga los datos y corre el ciclo login → menú."""
    # Crear servicios (única fuente de verdad de las colecciones)
    categoria_servicio = CategoriaServicio()
    producto_servicio = ProductoServicio(categoria_servicio)
    usuario_servicio = UsuarioServicio()
    pedido_servicio = PedidoServicio(usuario_servicio, producto_servicio)

    # Datos iniciales
    cargar_datos_iniciales(usuario_servicio, categoria_servicio, producto_servicio)

    try:
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
    except (KeyboardInterrupt, EOFError):
        print("\n\nPrograma interrumpido. ¡Hasta luego!")

if __name__ == "__main__":
    main()
