from entidades import Usuario
from excepciones import FoodStoreError
from servicios import (
    CategoriaServicio,
    ProductoServicio,
    UsuarioServicio,
    PedidoServicio,
)
from consola.menu import Menu
from consola.utilidades import pedir_entero, pausa


class MenuCliente(Menu):
    """Menú de solo consulta para el rol USUARIO."""

    def mostrar(self) -> bool:
        while True:
            print("\n" + "=" * 50)
            print(f"=== FOOD STORE  CLIENTE ({self._usuario.nombre_completo()}) ===")
            print("=" * 50)
            print("1. Ver categorías")
            print("2. Ver productos disponibles")
            print("3. Mis pedidos")
            print("4. Mis datos")
            print("9. Cerrar sesión")
            print("0. Salir")
            opcion = input("Seleccione: ").strip()

            try:
                if opcion == "1":
                    self._ver_categorias()
                elif opcion == "2":
                    self._ver_productos()
                elif opcion == "3":
                    self._mis_pedidos()
                elif opcion == "4":
                    self._mis_datos()
                elif opcion == "9":
                    print("\nSesión cerrada.")
                    return True
                elif opcion == "0":
                    print("\n¡Hasta luego!")
                    return False
                else:
                    print("   Opción inválida.")
            except FoodStoreError as e:
                print(f"   {e.mensaje}")
            except ValueError:
                print("   Valor numérico inválido.")
            pausa()

    def _ver_categorias(self) -> None:
        cats = self._categoria_servicio.listar()
        if not cats:
            print("No hay categorías cargadas.")
            return
        print("\nCategorías:")
        for c in cats:
            print(f"  {c}")

    def _ver_productos(self) -> None:
        prods = self._producto_servicio.listar(solo_disponibles_con_stock=True)
        if not prods:
            print("No hay productos disponibles con stock.")
            return
        print("\nProductos disponibles:")
        for p in prods:
            print(f"  {p}")

    def _mis_pedidos(self) -> None:
        pedidos = self._pedido_servicio.listar(id_usuario=self._usuario.id)
        if not pedidos:
            print("No tenés pedidos registrados.")
            return
        print("\nMis pedidos:")
        for p in pedidos:
            print(f"  {p}")

        if pedir_si_no_simple("¿Ver detalles de algún pedido?"):
            id_ped = pedir_entero("Id del pedido: ", minimo=1)
            # Solo permite ver los propios
            pedido = self._pedido_servicio.buscar_por_id(id_ped)
            if pedido.usuario.id != self._usuario.id:
                print("   Pedido no encontrado.")
                return
            print(f"\n{pedido}")
            print("  Detalles:")
            for d in pedido.detalles:
                print(f"  {d}")
            print(f"  TOTAL: ${pedido.total:.2f}")

    def _mis_datos(self) -> None:
        u = self._usuario
        print("\nMis datos:")
        print(f"  Nombre:    {u.nombre}")
        print(f"  Apellido:  {u.apellido}")
        print(f"  Mail:      {u.mail}")
        print(f"  Celular:   {u.celular}")
        print(f"  Rol:       {u.rol}")


def pedir_si_no_simple(mensaje: str) -> bool:
    valor = input(f"{mensaje} (S/N): ").strip().upper()
    return valor in ("S", "SI", "SÍ")
