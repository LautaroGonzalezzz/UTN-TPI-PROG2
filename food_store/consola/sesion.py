import getpass
from typing import Optional

from consola.estilos import GRIS, banner, error, exito, info, limpiar_pantalla, pintar, titulo
from entidades import Usuario
from excepciones import CredencialesInvalidasError
from servicios import UsuarioServicio

MAX_INTENTOS: int = 3


def iniciar_sesion(usuario_servicio: UsuarioServicio) -> Optional[Usuario]:
    """Pide mail y contraseña (hasta 3 intentos). Devuelve el usuario o None si se agotan."""
    limpiar_pantalla()
    banner()
    print(pintar(" Demo: admin@foodstore.com / admin123 · juan@cliente.com / cliente123", GRIS))
    print()
    titulo("=== FOOD STORE – INICIO DE SESIÓN ===")
    for intento in range(1, MAX_INTENTOS + 1):
        mail: str = input("Mail: ").strip()
        contrasenia: str = getpass.getpass("Contraseña: ")
        try:
            usuario: Usuario = usuario_servicio.autenticar(mail, contrasenia)
        except CredencialesInvalidasError as e:
            error(e.mensaje)
            restantes: int = MAX_INTENTOS - intento
            if restantes > 0:
                info(f"Intentos restantes: {restantes}")
            continue
        print()
        exito(f"Bienvenido/a, {usuario.nombre_completo()} [{usuario.rol}]")
        input(pintar("\nPresione Enter para continuar...", GRIS))
        return usuario
    error("Se agotaron los 3 intentos. El programa finalizará.")
    return None
