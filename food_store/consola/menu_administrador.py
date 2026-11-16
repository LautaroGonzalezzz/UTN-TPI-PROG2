from typing import Any

from consola.estilos import exito, info
from consola.menu import Menu, Opcion
from consola.utilidades import (
    pedir_entero,
    pedir_enum,
    pedir_enum_opcional,
    pedir_float,
    pedir_si_no,
    pedir_si_no_opcional,
    pedir_texto,
)
from consola.vistas import (
    mostrar_categorias,
    mostrar_detalle_pedido,
    mostrar_pedidos,
    mostrar_productos,
    mostrar_usuarios,
)
from enums import Estado, FormaPago, Rol
from formato import formato_pesos


class MenuAdministrador(Menu):
    """Menú completo de gestión para el rol ADMIN."""

    def mostrar(self) -> bool:
        opciones: list[Opcion] = [
            ("1", "Categorías", self._submenu_categorias),
            ("2", "Productos", self._submenu_productos),
            ("3", "Usuarios", self._submenu_usuarios),
            ("4", "Pedidos", self._submenu_pedidos),
        ]
        titulo: str = f"=== FOOD STORE – ADMINISTRADOR ({self._usuario.nombre_completo()}) ==="
        return self._ejecutar_menu_principal(titulo, opciones, pausar=False)

    # ------------------------------------------------------------------
    # Categorías
    # ------------------------------------------------------------------
    def _submenu_categorias(self) -> None:
        self._ejecutar_submenu(
            "--- CATEGORÍAS ---",
            [
                ("1", "Listar", self._listar_categorias),
                ("2", "Crear", self._crear_categoria),
                ("3", "Editar", self._editar_categoria),
                ("4", "Eliminar", self._eliminar_categoria),
            ],
        )

    def _listar_categorias(self) -> None:
        mostrar_categorias(self._categoria_servicio.listar())

    def _crear_categoria(self) -> None:
        nombre: str = pedir_texto("Nombre: ")
        descripcion: str = pedir_texto("Descripción: ")
        categoria = self._categoria_servicio.crear(nombre, descripcion)
        exito(f"Categoría creada con id {categoria.id}")

    def _editar_categoria(self) -> None:
        self._listar_categorias()
        id_categoria: int = pedir_entero("Id de la categoría a editar: ", minimo=1)
        nombre: str = pedir_texto("Nuevo nombre (Enter = conservar): ", permitir_vacio=True)
        descripcion: str = pedir_texto("Nueva descripción (Enter = conservar): ", permitir_vacio=True)
        categoria = self._categoria_servicio.editar(
            id_categoria,
            nombre=nombre or None,
            descripcion=descripcion or None,
        )
        exito(f"Categoría actualizada: {categoria}")

    def _eliminar_categoria(self) -> None:
        self._listar_categorias()
        id_categoria: int = pedir_entero("Id de la categoría a eliminar: ", minimo=1)
        if not pedir_si_no("¿Confirma la baja lógica?"):
            info("Operación cancelada.")
            return
        self._categoria_servicio.eliminar(id_categoria, self._producto_servicio.todos())
        exito("Categoría eliminada (baja lógica).")

    # ------------------------------------------------------------------
    # Productos
    # ------------------------------------------------------------------
    def _submenu_productos(self) -> None:
        self._ejecutar_submenu(
            "--- PRODUCTOS ---",
            [
                ("1", "Listar", self._listar_productos),
                ("2", "Crear", self._crear_producto),
                ("3", "Editar", self._editar_producto),
                ("4", "Eliminar", self._eliminar_producto),
            ],
        )

    def _listar_productos(self) -> None:
        mostrar_productos(self._producto_servicio.listar(), "No hay productos cargados.")

    def _crear_producto(self) -> None:
        self._listar_categorias()
        nombre: str = pedir_texto("Nombre: ")
        descripcion: str = pedir_texto("Descripción: ")
        precio: float = pedir_float("Precio: ", minimo=0)
        stock: int = pedir_entero("Stock: ", minimo=0)
        imagen: str = pedir_texto("URL/imagen (puede quedar vacío): ", permitir_vacio=True)
        disponible: bool = pedir_si_no("¿Disponible?")
        id_categoria: int = pedir_entero("Id de categoría: ", minimo=1)
        producto = self._producto_servicio.crear(
            nombre, precio, descripcion, stock, imagen, disponible, id_categoria
        )
        exito(f"Producto creado con id {producto.id}")

    def _editar_producto(self) -> None:
        self._listar_productos()
        id_producto: int = pedir_entero("Id del producto a editar: ", minimo=1)
        nombre: str = pedir_texto("Nuevo nombre (Enter = conservar): ", permitir_vacio=True)
        precio: str = pedir_texto("Nuevo precio (Enter = conservar): ", permitir_vacio=True)
        descripcion: str = pedir_texto("Nueva descripción (Enter = conservar): ", permitir_vacio=True)
        stock: str = pedir_texto("Nuevo stock (Enter = conservar): ", permitir_vacio=True)
        imagen: str = pedir_texto("Nueva imagen (Enter = conservar): ", permitir_vacio=True)
        disponible: bool | None = pedir_si_no_opcional("¿Disponible?")
        self._listar_categorias()
        id_categoria: str = pedir_texto("Id categoría (Enter = conservar): ", permitir_vacio=True)

        cambios: dict[str, Any] = {}
        if nombre:
            cambios["nombre"] = nombre
        if precio:
            cambios["precio"] = float(precio.replace(",", "."))
        if descripcion:
            cambios["descripcion"] = descripcion
        if stock:
            cambios["stock"] = int(stock)
        if imagen:
            cambios["imagen"] = imagen
        if disponible is not None:
            cambios["disponible"] = disponible
        if id_categoria:
            cambios["id_categoria"] = int(id_categoria)

        producto = self._producto_servicio.editar(id_producto, **cambios)
        exito(f"Producto actualizado: {producto}")

    def _eliminar_producto(self) -> None:
        self._listar_productos()
        id_producto: int = pedir_entero("Id del producto a eliminar: ", minimo=1)
        if not pedir_si_no("¿Confirma la baja lógica?"):
            info("Operación cancelada.")
            return
        self._producto_servicio.eliminar(id_producto)
        exito("Producto eliminado (baja lógica).")

    # ------------------------------------------------------------------
    # Usuarios
    # ------------------------------------------------------------------
    def _submenu_usuarios(self) -> None:
        self._ejecutar_submenu(
            "--- USUARIOS ---",
            [
                ("1", "Listar", self._listar_usuarios),
                ("2", "Crear", self._crear_usuario),
                ("3", "Editar", self._editar_usuario),
                ("4", "Eliminar", self._eliminar_usuario),
            ],
        )

    def _listar_usuarios(self) -> None:
        mostrar_usuarios(self._usuario_servicio.listar())

    def _crear_usuario(self) -> None:
        nombre: str = pedir_texto("Nombre: ")
        apellido: str = pedir_texto("Apellido: ")
        mail: str = pedir_texto("Mail: ")
        celular: str = pedir_texto("Celular: ")
        contrasenia: str = pedir_texto("Contraseña: ")
        rol: Rol = pedir_enum("Rol:", Rol)
        usuario = self._usuario_servicio.crear(nombre, apellido, mail, celular, contrasenia, rol)
        exito(f"Usuario creado con id {usuario.id}")

    def _editar_usuario(self) -> None:
        self._listar_usuarios()
        id_usuario: int = pedir_entero("Id del usuario a editar: ", minimo=1)
        nombre: str = pedir_texto("Nuevo nombre (Enter = conservar): ", permitir_vacio=True)
        apellido: str = pedir_texto("Nuevo apellido (Enter = conservar): ", permitir_vacio=True)
        mail: str = pedir_texto("Nuevo mail (Enter = conservar): ", permitir_vacio=True)
        celular: str = pedir_texto("Nuevo celular (Enter = conservar): ", permitir_vacio=True)
        contrasenia: str = pedir_texto("Nueva contraseña (Enter = conservar): ", permitir_vacio=True)
        rol: Rol | None = pedir_enum_opcional("Rol:", Rol)

        cambios: dict[str, Any] = {}
        if nombre:
            cambios["nombre"] = nombre
        if apellido:
            cambios["apellido"] = apellido
        if mail:
            cambios["mail"] = mail
        if celular:
            cambios["celular"] = celular
        if contrasenia:
            cambios["contrasenia"] = contrasenia
        if rol is not None:
            cambios["rol"] = rol

        usuario = self._usuario_servicio.editar(id_usuario, **cambios)
        exito(f"Usuario actualizado: {usuario}")

    def _eliminar_usuario(self) -> None:
        self._listar_usuarios()
        id_usuario: int = pedir_entero("Id del usuario a eliminar: ", minimo=1)
        if not pedir_si_no("¿Confirma la baja lógica?"):
            info("Operación cancelada.")
            return
        self._usuario_servicio.eliminar(id_usuario, self._usuario)
        exito("Usuario eliminado (baja lógica).")

    # ------------------------------------------------------------------
    # Pedidos
    # ------------------------------------------------------------------
    def _submenu_pedidos(self) -> None:
        self._ejecutar_submenu(
            "--- PEDIDOS ---",
            [
                ("1", "Listar", self._listar_pedidos),
                ("2", "Crear", self._crear_pedido),
                ("3", "Cambiar estado / forma de pago", self._actualizar_pedido),
                ("4", "Eliminar", self._eliminar_pedido),
                ("5", "Ver detalles de un pedido", self._ver_detalles_pedido),
            ],
        )

    def _listar_pedidos(self) -> None:
        mostrar_pedidos(self._pedido_servicio.listar(), "No hay pedidos cargados.")

    def _crear_pedido(self) -> None:
        self._listar_usuarios()
        id_usuario: int = pedir_entero("Id del usuario: ", minimo=1)
        forma_pago: FormaPago = pedir_enum("Forma de pago:", FormaPago)

        disponibles = self._producto_servicio.listar(solo_disponibles_con_stock=True)
        if not disponibles:
            info("No hay productos disponibles con stock.")
            return
        mostrar_productos(disponibles, "")

        items: list[tuple[int, int]] = []
        while True:
            id_producto: int = pedir_entero("Id de producto (0 para terminar): ", minimo=0)
            if id_producto == 0:
                break
            cantidad: int = pedir_entero("Cantidad: ", minimo=1)
            items.append((id_producto, cantidad))
            if not pedir_si_no("¿Agregar otro producto?"):
                break

        if not items:
            info("No se agregaron productos. Pedido cancelado.")
            return

        pedido = self._pedido_servicio.crear(id_usuario, forma_pago, items)
        exito(f"Pedido creado con id {pedido.id} | Total: {formato_pesos(pedido.total)}")

    def _actualizar_pedido(self) -> None:
        self._listar_pedidos()
        id_pedido: int = pedir_entero("Id del pedido: ", minimo=1)
        print("1. Cambiar estado")
        print("2. Cambiar forma de pago")
        print("3. Ambos")
        opcion: int = pedir_entero("Seleccione: ", minimo=1, maximo=3)

        if opcion in (1, 3):
            estado: Estado = pedir_enum("Nuevo estado:", Estado)
            self._pedido_servicio.cambiar_estado(id_pedido, estado)
            exito(f"Estado actualizado a {estado}")
        if opcion in (2, 3):
            forma_pago: FormaPago = pedir_enum("Nueva forma de pago:", FormaPago)
            self._pedido_servicio.cambiar_forma_pago(id_pedido, forma_pago)
            exito(f"Forma de pago actualizada a {forma_pago}")

    def _eliminar_pedido(self) -> None:
        self._listar_pedidos()
        id_pedido: int = pedir_entero("Id del pedido a eliminar: ", minimo=1)
        if not pedir_si_no("¿Confirma la baja lógica?"):
            info("Operación cancelada.")
            return
        self._pedido_servicio.eliminar(id_pedido)
        exito("Pedido eliminado (baja lógica).")

    def _ver_detalles_pedido(self) -> None:
        self._listar_pedidos()
        id_pedido: int = pedir_entero("Id del pedido: ", minimo=1)
        mostrar_detalle_pedido(self._pedido_servicio.buscar_por_id(id_pedido))
