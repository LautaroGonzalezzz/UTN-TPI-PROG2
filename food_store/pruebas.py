"""
Pruebas del modelo y de los servicios (sin menú de consola).
Ejecutar: python pruebas.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from enums import Rol, Estado, FormaPago
from excepciones import (
    FoodStoreError,
    EntidadNoEncontradaError,
    DatoInvalidoError,
    PrecioInvalidoError,
    StockInsuficienteError,
    DuplicadoError,
    OperacionNoPermitidaError,
    CredencialesInvalidasError,
)
from entidades import Categoria, Producto, Usuario, Pedido, DetallePedido
from servicios import (
    CategoriaServicio,
    ProductoServicio,
    UsuarioServicio,
    PedidoServicio,
)


def ok(msg: str) -> None:
    print(f"  – {msg}")


def error_esperado(msg: str) -> None:
    print(f"  – Error esperado: {msg}")


def seccion(titulo: str) -> None:
    print(f"\n{'='*60}\n{titulo}\n{'='*60}")


def probar_entidades() -> None:
    seccion("1. ENTIDADES – Constructores, encapsulamiento y validaciones")

    # Categoría
    cat = Categoria("Pizzas", "Las mejores pizzas")
    assert cat.id > 0
    assert not cat.eliminado
    assert cat.nombre == "Pizzas"
    ok(f"Categoria creada: {cat}")

    try:
        cat.nombre = "   "
        assert False, "Debió lanzar DatoInvalidoError"
    except DatoInvalidoError as e:
        error_esperado(str(e))

    # Producto
    prod = Producto("Muzzarella", 8000.0, "Clásica", 10, "img.jpg", True, cat)
    assert prod.precio == 8000.0
    assert prod.categoria is cat
    ok(f"Producto creado: {prod}")

    try:
        prod.precio = -1
        assert False
    except PrecioInvalidoError as e:
        error_esperado(str(e))

    try:
        prod.stock = -5
        assert False
    except DatoInvalidoError as e:
        error_esperado(str(e))

    # Usuario
    user = Usuario("Ana", "Pérez", "ana@test.com", "123", "pass123", Rol.ADMIN)
    assert user.verificar_contrasenia("pass123")
    assert not user.verificar_contrasenia("otra")
    ok(f"Usuario creado: {user}")

    try:
        _ = user.contrasenia  # no debe poder leerse
        assert False
    except AttributeError:
        ok("contraseña no tiene property de lectura")

    # Pedido + Detalle (composición)
    pedido = Pedido(user, FormaPago.EFECTIVO)
    pedido.agregar_detalle(2, prod)
    assert len(pedido.detalles) == 1
    assert pedido.total == 16000.0
    ok(f"Pedido con detalle: {pedido}")
    ok(f"  Detalle: {pedido.detalles[0]}")

    # No se puede modificar la lista de detalles desde afuera
    detalles = pedido.detalles
    assert isinstance(detalles, tuple)
    ok("detalles devuelve tupla (inmutable)")

    # Sumar cantidad al mismo producto
    pedido.agregar_detalle(1, prod)
    assert pedido.detalles[0].cantidad == 3
    assert pedido.total == 24000.0
    ok("agregar_detalle suma cantidad si el producto ya existe")

    # Stock insuficiente
    try:
        pedido.agregar_detalle(100, prod)
        assert False
    except StockInsuficienteError as e:
        error_esperado(str(e))

    # Transición de estado
    pedido.estado = Estado.CONFIRMADO
    ok(f"Estado  CONFIRMADO")
    try:
        pedido.estado = Estado.PENDIENTE
        assert False
    except OperacionNoPermitidaError as e:
        error_esperado(str(e))

    pedido.estado = Estado.CANCELADO
    ok("Estado  CANCELADO (desde CONFIRMADO)")


def probar_servicios() -> None:
    seccion("2. SERVICIOS – Colecciones y reglas de negocio")

    cat_srv = CategoriaServicio()
    prod_srv = ProductoServicio(cat_srv)
    user_srv = UsuarioServicio()
    ped_srv = PedidoServicio(user_srv, prod_srv)

    # --- Categorías ---
    c1 = cat_srv.crear("Bebidas", "Gaseosas y jugos")
    c2 = cat_srv.crear("Postres", "Dulces")
    ok(f"Categorías creadas: {c1.id}, {c2.id}")

    try:
        cat_srv.crear("bebidas", "otra")  # case-insensitive
        assert False
    except DuplicadoError as e:
        error_esperado(str(e))

    # --- Productos ---
    p1 = prod_srv.crear("Coca", 2000.0, "1.5L", 30, "", True, c1.id)
    p2 = prod_srv.crear("Flan", 1500.0, "Casero", 5, "", True, c2.id)
    ok(f"Productos creados: {p1.id}, {p2.id}")

    # --- Usuarios ---
    admin = user_srv.crear("Admin", "Root", "admin@test.com", "111", "admin123", Rol.ADMIN)
    cliente = user_srv.crear("Juan", "Cliente", "juan@test.com", "222", "cli123", Rol.USUARIO)
    ok(f"Usuarios: {admin}, {cliente}")

    try:
        user_srv.crear("Otro", "User", "admin@test.com", "333", "x", Rol.USUARIO)
        assert False
    except DuplicadoError as e:
        error_esperado(str(e))

    # Autenticación
    u = user_srv.autenticar("admin@test.com", "admin123")
    assert u.id == admin.id
    ok("Autenticación correcta")

    try:
        user_srv.autenticar("admin@test.com", "mala")
        assert False
    except CredencialesInvalidasError as e:
        error_esperado(str(e))

    try:
        user_srv.autenticar("noexiste@test.com", "x")
        assert False
    except CredencialesInvalidasError as e:
        error_esperado(str(e))

    # --- Pedidos ---
    pedido = ped_srv.crear(
        cliente.id,
        FormaPago.TARJETA,
        [(p1.id, 2), (p2.id, 1)],
    )
    assert pedido.total == 2 * 2000 + 1500
    assert p1.stock == 28  # 30 - 2
    assert p2.stock == 4   # 5 - 1
    ok(f"Pedido creado: {pedido} | stock actualizado")

    # Fallo por stock  no se crea ni se descuenta
    stock_antes = p2.stock
    try:
        ped_srv.crear(cliente.id, FormaPago.EFECTIVO, [(p2.id, 100)])
        assert False
    except StockInsuficienteError as e:
        error_esperado(str(e))
    assert p2.stock == stock_antes
    ok("Al fallar por stock el pedido no se agrega ni modifica stock")

    # Cancelar  devuelve stock
    ped_srv.cambiar_estado(pedido.id, Estado.CONFIRMADO)
    ped_srv.cambiar_estado(pedido.id, Estado.CANCELADO)
    assert p1.stock == 30
    assert p2.stock == 5
    ok("Al cancelar se devuelve el stock")

    # Eliminar categoría con productos activos
    try:
        cat_srv.eliminar(c1.id, prod_srv.todos())
        assert False
    except OperacionNoPermitidaError as e:
        error_esperado(str(e))

    # Baja lógica de producto
    prod_srv.eliminar(p1.id)
    assert p1.eliminado
    assert len(prod_srv.listar()) == 1  # solo p2
    ok("Baja lógica de producto funciona")

    # Admin no puede autoeliminarse
    try:
        user_srv.eliminar(admin.id, admin)
        assert False
    except OperacionNoPermitidaError as e:
        error_esperado(str(e))

    # Baja lógica de usuario
    user_srv.eliminar(cliente.id, admin)
    assert cliente.eliminado
    try:
        user_srv.autenticar("juan@test.com", "cli123")
        assert False
    except CredencialesInvalidasError:
        ok("Usuario eliminado no puede iniciar sesión")


def probar_correcciones() -> None:
    seccion("3. CORRECCIONES  Base abstracta, mail reutilizado y ediciones atómicas")
    from entidades import Base
    try:
        Base()
        assert False, "Base no debería instanciarse"
    except TypeError:
        ok("Base es abstracta: no se puede instanciar")

    user_srv = UsuarioServicio()
    admin = user_srv.crear("Ana", "Pérez", "a@t.com", "1", "x", Rol.ADMIN)
    viejo = user_srv.crear("Juan", "Viejo", "j@t.com", "1", "viejo", Rol.USUARIO)
    user_srv.eliminar(viejo.id, admin)
    user_srv.crear("Juan", "Nuevo", "j@t.com", "1", "nuevo", Rol.USUARIO)
    user_srv.autenticar("j@t.com", "nuevo")
    ok("Un mail de usuario dado de baja se puede reutilizar y el nuevo inicia sesión")

    otro = user_srv.crear("Luis", "R", "l@t.com", "1", "pw", Rol.USUARIO)
    try:
        user_srv.editar(otro.id, nombre="Cambiado", mail="a@t.com")
        assert False
    except DuplicadoError:
        assert otro.nombre == "Luis"
        error_esperado("mail duplicado al editar; no se modificó ningún campo")

    cat_srv = CategoriaServicio()
    prod_srv = ProductoServicio(cat_srv)
    cat = cat_srv.crear("Pizzas", "desc")
    prod = prod_srv.crear("Muza", 100.0, "d", 5, "", True, cat.id)
    try:
        prod_srv.editar(prod.id, precio=999.0, stock=-1)
        assert False
    except DatoInvalidoError:
        assert prod.precio == 100.0 and prod.stock == 5
        error_esperado("stock negativo al editar; el precio se restauró a 100.0")

    try:
        _ = admin.contrasenia
        assert False
    except AttributeError:
        ok("La contraseña no se puede leer")


def probar_formato_y_vistas() -> None:
    seccion("4. FORMATO Y VISTAS  Pesos, fechas y tablas de consola")
    from datetime import date

    from consola.estilos import tabla
    from formato import formato_fecha, formato_pesos

    assert formato_pesos(8500) == "$8.500,00"
    assert formato_pesos(1234567.5) == "$1.234.567,50"
    assert formato_fecha(date(2026, 11, 16)) == "16/11/2026"
    ok("formato_pesos y formato_fecha devuelven el formato argentino")

    cat = Categoria("Pizzas", "desc")
    prod = Producto("Muzzarella", 8500.0, "d", 3, "", True, cat)
    assert "$8.500,00" in str(prod)
    tabla(["ID", "Producto", "Precio"], [[str(prod.id), prod.nombre, formato_pesos(prod.precio)]], "rlr")
    ok("tabla se imprime alineada (arriba)")


def main() -> None:
    print("\n*** PRUEBAS FOOD STORE ***\n")
    try:
        probar_entidades()
        probar_servicios()
        probar_correcciones()
        probar_formato_y_vistas()
        print("\n" + "=" * 60)
        print("TODAS LAS PRUEBAS PASARON CORRECTAMENTE")
        print("=" * 60 + "\n")
    except AssertionError as e:
        print(f"\n FALLO DE ASSERT: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n ERROR INESPERADO: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
