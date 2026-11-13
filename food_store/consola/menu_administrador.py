from entidades import Usuario
from enums import Rol, Estado, FormaPago
from excepciones import FoodStoreError
from servicios import (
    CategoriaServicio,
    ProductoServicio,
    UsuarioServicio,
    PedidoServicio,
)
from consola.menu import Menu
from consola.utilidades import (
    pedir_texto,
    pedir_entero,
    pedir_float,
    pedir_si_no,
    pedir_enum,
    pausa,
)


class MenuAdministrador(Menu):
    """Menú completo de gestión para el rol ADMIN."""

    def mostrar(self) -> bool:
        while True:
            print("\n" + "=" * 50)
            print(f"=== FOOD STORE  ADMINISTRADOR ({self._usuario.nombre_completo()}) ===")
            print("=" * 50)
            print("1. Categorías")
            print("2. Productos")
            print("3. Usuarios")
            print("4. Pedidos")
            print("9. Cerrar sesión")
            print("0. Salir")
            opcion = input("Seleccione: ").strip()

            if opcion == "1":
                self._submenu_categorias()
            elif opcion == "2":
                self._submenu_productos()
            elif opcion == "3":
                self._submenu_usuarios()
            elif opcion == "4":
                self._submenu_pedidos()
            elif opcion == "9":
                print("\nSesión cerrada.")
                return True
            elif opcion == "0":
                print("\n¡Hasta luego!")
                return False
            else:
                print("   Opción inválida.")

    # ------------------------------------------------------------------
    # Categorías
    # ------------------------------------------------------------------
    def _submenu_categorias(self) -> None:
        while True:
            print("\n--- CATEGORÍAS ---")
            print("1. Listar")
            print("2. Crear")
            print("3. Editar")
            print("4. Eliminar")
            print("0. Volver")
            op = input("Seleccione: ").strip()
            try:
                if op == "1":
                    self._listar_categorias()
                elif op == "2":
                    self._crear_categoria()
                elif op == "3":
                    self._editar_categoria()
                elif op == "4":
                    self._eliminar_categoria()
                elif op == "0":
                    return
                else:
                    print("   Opción inválida.")
            except FoodStoreError as e:
                print(f"   {e.mensaje}")
            except ValueError:
                print("   Valor numérico inválido.")
            pausa()

    def _listar_categorias(self) -> None:
        cats = self._categoria_servicio.listar()
        if not cats:
            print("No hay categorías cargadas.")
            return
        print("\nCategorías:")
        for c in cats:
            print(f"  {c}")

    def _crear_categoria(self) -> None:
        nombre = pedir_texto("Nombre: ")
        descripcion = pedir_texto("Descripción: ")
        cat = self._categoria_servicio.crear(nombre, descripcion)
        print(f"   Categoría creada con id {cat.id}")

    def _editar_categoria(self) -> None:
        self._listar_categorias()
        id_cat = pedir_entero("Id de la categoría a editar: ", minimo=1)
        nombre = pedir_texto("Nuevo nombre (Enter = conservar): ", permitir_vacio=True)
        descripcion = pedir_texto("Nueva descripción (Enter = conservar): ", permitir_vacio=True)
        cat = self._categoria_servicio.editar(
            id_cat,
            nombre=nombre if nombre else None,
            descripcion=descripcion if descripcion else None,
        )
        print(f"   Categoría actualizada: {cat}")

    def _eliminar_categoria(self) -> None:
        self._listar_categorias()
        id_cat = pedir_entero("Id de la categoría a eliminar: ", minimo=1)
        if not pedir_si_no("¿Confirma la baja lógica?"):
            print("  Operación cancelada.")
            return
        productos = self._producto_servicio.todos()
        self._categoria_servicio.eliminar(id_cat, productos)
        print("   Categoría eliminada (baja lógica).")

    # ------------------------------------------------------------------
    # Productos
    # ------------------------------------------------------------------
    def _submenu_productos(self) -> None:
        while True:
            print("\n--- PRODUCTOS ---")
            print("1. Listar")
            print("2. Crear")
            print("3. Editar")
            print("4. Eliminar")
            print("0. Volver")
            op = input("Seleccione: ").strip()
            try:
                if op == "1":
                    self._listar_productos()
                elif op == "2":
                    self._crear_producto()
                elif op == "3":
                    self._editar_producto()
                elif op == "4":
                    self._eliminar_producto()
                elif op == "0":
                    return
                else:
                    print("   Opción inválida.")
            except FoodStoreError as e:
                print(f"   {e.mensaje}")
            except ValueError:
                print("   Valor numérico inválido.")
            pausa()

    def _listar_productos(self) -> None:
        prods = self._producto_servicio.listar()
        if not prods:
            print("No hay productos cargados.")
            return
        print("\nProductos:")
        for p in prods:
            print(f"  {p}")

    def _crear_producto(self) -> None:
        self._listar_categorias()
        nombre = pedir_texto("Nombre: ")
        descripcion = pedir_texto("Descripción: ")
        precio = pedir_float("Precio: ", minimo=0)
        stock = pedir_entero("Stock: ", minimo=0)
        imagen = pedir_texto("URL/imagen (puede quedar vacío): ", permitir_vacio=True)
        disponible = pedir_si_no("¿Disponible?")
        id_cat = pedir_entero("Id de categoría: ", minimo=1)
        prod = self._producto_servicio.crear(
            nombre, precio, descripcion, stock, imagen, disponible, id_cat
        )
        print(f"   Producto creado con id {prod.id}")

    def _editar_producto(self) -> None:
        self._listar_productos()
        id_prod = pedir_entero("Id del producto a editar: ", minimo=1)
        nombre = pedir_texto("Nuevo nombre (Enter = conservar): ", permitir_vacio=True)
        precio_str = pedir_texto("Nuevo precio (Enter = conservar): ", permitir_vacio=True)
        descripcion = pedir_texto("Nueva descripción (Enter = conservar): ", permitir_vacio=True)
        stock_str = pedir_texto("Nuevo stock (Enter = conservar): ", permitir_vacio=True)
        imagen = pedir_texto("Nueva imagen (Enter = conservar): ", permitir_vacio=True)
        print("Disponible: 1=Sí  2=No  Enter=conservar")
        disp_str = input("Seleccione: ").strip()
        self._listar_categorias()
        id_cat_str = pedir_texto("Id categoría (Enter = conservar): ", permitir_vacio=True)

        kwargs: dict = {}
        if nombre:
            kwargs["nombre"] = nombre
        if precio_str:
            kwargs["precio"] = float(precio_str.replace(",", "."))
        if descripcion:
            kwargs["descripcion"] = descripcion
        if stock_str:
            kwargs["stock"] = int(stock_str)
        if imagen:
            kwargs["imagen"] = imagen
        if disp_str == "1":
            kwargs["disponible"] = True
        elif disp_str == "2":
            kwargs["disponible"] = False
        if id_cat_str:
            kwargs["id_categoria"] = int(id_cat_str)

        prod = self._producto_servicio.editar(id_prod, **kwargs)
        print(f"   Producto actualizado: {prod}")

    def _eliminar_producto(self) -> None:
        self._listar_productos()
        id_prod = pedir_entero("Id del producto a eliminar: ", minimo=1)
        if not pedir_si_no("¿Confirma la baja lógica?"):
            print("  Operación cancelada.")
            return
        self._producto_servicio.eliminar(id_prod)
        print("   Producto eliminado (baja lógica).")

    # ------------------------------------------------------------------
    # Usuarios
    # ------------------------------------------------------------------
    def _submenu_usuarios(self) -> None:
        while True:
            print("\n--- USUARIOS ---")
            print("1. Listar")
            print("2. Crear")
            print("3. Editar")
            print("4. Eliminar")
            print("0. Volver")
            op = input("Seleccione: ").strip()
            try:
                if op == "1":
                    self._listar_usuarios()
                elif op == "2":
                    self._crear_usuario()
                elif op == "3":
                    self._editar_usuario()
                elif op == "4":
                    self._eliminar_usuario()
                elif op == "0":
                    return
                else:
                    print("   Opción inválida.")
            except FoodStoreError as e:
                print(f"   {e.mensaje}")
            except ValueError:
                print("   Valor numérico inválido.")
            pausa()

    def _listar_usuarios(self) -> None:
        users = self._usuario_servicio.listar()
        if not users:
            print("No hay usuarios cargados.")
            return
        print("\nUsuarios:")
        for u in users:
            print(f"  {u}")

    def _crear_usuario(self) -> None:
        nombre = pedir_texto("Nombre: ")
        apellido = pedir_texto("Apellido: ")
        mail = pedir_texto("Mail: ")
        celular = pedir_texto("Celular: ")
        contrasenia = pedir_texto("Contraseña: ")
        rol = pedir_enum("Rol:", Rol)
        user = self._usuario_servicio.crear(
            nombre, apellido, mail, celular, contrasenia, rol
        )
        print(f"   Usuario creado con id {user.id}")

    def _editar_usuario(self) -> None:
        self._listar_usuarios()
        id_user = pedir_entero("Id del usuario a editar: ", minimo=1)
        nombre = pedir_texto("Nuevo nombre (Enter = conservar): ", permitir_vacio=True)
        apellido = pedir_texto("Nuevo apellido (Enter = conservar): ", permitir_vacio=True)
        mail = pedir_texto("Nuevo mail (Enter = conservar): ", permitir_vacio=True)
        celular = pedir_texto("Nuevo celular (Enter = conservar): ", permitir_vacio=True)
        contrasenia = pedir_texto("Nueva contraseña (Enter = conservar): ", permitir_vacio=True)
        print("Rol: 1=ADMIN  2=USUARIO  Enter=conservar")
        rol_str = input("Seleccione: ").strip()

        kwargs: dict = {}
        if nombre:
            kwargs["nombre"] = nombre
        if apellido:
            kwargs["apellido"] = apellido
        if mail:
            kwargs["mail"] = mail
        if celular:
            kwargs["celular"] = celular
        if contrasenia:
            kwargs["contrasenia"] = contrasenia
        if rol_str == "1":
            kwargs["rol"] = Rol.ADMIN
        elif rol_str == "2":
            kwargs["rol"] = Rol.USUARIO

        user = self._usuario_servicio.editar(id_user, **kwargs)
        print(f"   Usuario actualizado: {user}")

    def _eliminar_usuario(self) -> None:
        self._listar_usuarios()
        id_user = pedir_entero("Id del usuario a eliminar: ", minimo=1)
        if not pedir_si_no("¿Confirma la baja lógica?"):
            print("  Operación cancelada.")
            return
        self._usuario_servicio.eliminar(id_user, self._usuario)
        print("   Usuario eliminado (baja lógica).")

    # ------------------------------------------------------------------
    # Pedidos
    # ------------------------------------------------------------------
    def _submenu_pedidos(self) -> None:
        while True:
            print("\n--- PEDIDOS ---")
            print("1. Listar")
            print("2. Crear")
            print("3. Cambiar estado / forma de pago")
            print("4. Eliminar")
            print("5. Ver detalles de un pedido")
            print("0. Volver")
            op = input("Seleccione: ").strip()
            try:
                if op == "1":
                    self._listar_pedidos()
                elif op == "2":
                    self._crear_pedido()
                elif op == "3":
                    self._actualizar_pedido()
                elif op == "4":
                    self._eliminar_pedido()
                elif op == "5":
                    self._ver_detalles_pedido()
                elif op == "0":
                    return
                else:
                    print("   Opción inválida.")
            except FoodStoreError as e:
                print(f"   {e.mensaje}")
            except ValueError:
                print("   Valor numérico inválido.")
            pausa()

    def _listar_pedidos(self) -> None:
        pedidos = self._pedido_servicio.listar()
        if not pedidos:
            print("No hay pedidos cargados.")
            return
        print("\nPedidos:")
        for p in pedidos:
            print(f"  {p}")

    def _crear_pedido(self) -> None:
        self._listar_usuarios()
        id_user = pedir_entero("Id del usuario: ", minimo=1)
        forma = pedir_enum("Forma de pago:", FormaPago)

        # Listar productos disponibles
        prods = self._producto_servicio.listar(solo_disponibles_con_stock=True)
        if not prods:
            print("No hay productos disponibles con stock.")
            return
        print("\nProductos disponibles:")
        for p in prods:
            print(f"  {p}")

        items: list[tuple[int, int]] = []
        while True:
            id_prod = pedir_entero("Id de producto (0 para terminar): ", minimo=0)
            if id_prod == 0:
                break
            cantidad = pedir_entero("Cantidad: ", minimo=1)
            items.append((id_prod, cantidad))
            if not pedir_si_no("¿Agregar otro producto?"):
                break

        if not items:
            print("   No se agregaron productos. Pedido cancelado.")
            return

        pedido = self._pedido_servicio.crear(id_user, forma, items)
        print(f"   Pedido creado con id {pedido.id} | Total: ${pedido.total:.2f}")

    def _actualizar_pedido(self) -> None:
        self._listar_pedidos()
        id_ped = pedir_entero("Id del pedido: ", minimo=1)
        print("1. Cambiar estado")
        print("2. Cambiar forma de pago")
        print("3. Ambos")
        sub = input("Seleccione: ").strip()

        if sub in ("1", "3"):
            estado = pedir_enum("Nuevo estado:", Estado)
            self._pedido_servicio.cambiar_estado(id_ped, estado)
            print(f"   Estado actualizado a {estado}")
        if sub in ("2", "3"):
            forma = pedir_enum("Nueva forma de pago:", FormaPago)
            self._pedido_servicio.cambiar_forma_pago(id_ped, forma)
            print(f"   Forma de pago actualizada a {forma}")
        if sub not in ("1", "2", "3"):
            print("   Opción inválida.")

    def _eliminar_pedido(self) -> None:
        self._listar_pedidos()
        id_ped = pedir_entero("Id del pedido a eliminar: ", minimo=1)
        if not pedir_si_no("¿Confirma la baja lógica?"):
            print("  Operación cancelada.")
            return
        self._pedido_servicio.eliminar(id_ped)
        print("   Pedido eliminado (baja lógica).")

    def _ver_detalles_pedido(self) -> None:
        self._listar_pedidos()
        id_ped = pedir_entero("Id del pedido: ", minimo=1)
        pedido = self._pedido_servicio.buscar_por_id(id_ped)
        print(f"\n{pedido}")
        if not pedido.detalles:
            print("  (sin detalles)")
        else:
            print("  Detalles:")
            for d in pedido.detalles:
                print(f"  {d}")
            print(f"  TOTAL: ${pedido.total:.2f}")
