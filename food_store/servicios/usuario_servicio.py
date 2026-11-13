from typing import List, Optional

from entidades import Usuario
from enums import Rol
from excepciones import (
    EntidadNoEncontradaError,
    DuplicadoError,
    CredencialesInvalidasError,
    OperacionNoPermitidaError,
)


class UsuarioServicio:
    """Gestiona usuarios y autenticación."""

    def __init__(self) -> None:
        self.__usuarios: List[Usuario] = []

    def listar(self, solo_activos: bool = True) -> List[Usuario]:
        if solo_activos:
            return [u for u in self.__usuarios if not u.eliminado]
        return list(self.__usuarios)

    def buscar_por_id(self, id_usuario: int, solo_activos: bool = True) -> Usuario:
        for u in self.__usuarios:
            if u.id == id_usuario:
                if solo_activos and u.eliminado:
                    raise EntidadNoEncontradaError(
                        f"Usuario con id {id_usuario} no encontrado o eliminado"
                    )
                return u
        raise EntidadNoEncontradaError(
            f"Usuario con id {id_usuario} no encontrado"
        )

    def buscar_por_mail(self, mail: str, solo_activos: bool = True) -> Optional[Usuario]:
        mail_norm = mail.strip().lower()
        for u in self.__usuarios:
            if u.mail == mail_norm:
                if solo_activos and u.eliminado:
                    return None
                return u
        return None

    def _existe_mail(self, mail: str, excluir_id: Optional[int] = None) -> bool:
        mail_norm = mail.strip().lower()
        for u in self.__usuarios:
            if u.eliminado:
                continue
            if excluir_id is not None and u.id == excluir_id:
                continue
            if u.mail == mail_norm:
                return True
        return False

    def crear(
        self,
        nombre: str,
        apellido: str,
        mail: str,
        celular: str,
        contrasenia: str,
        rol: Rol,
    ) -> Usuario:
        if self._existe_mail(mail):
            raise DuplicadoError(f"Ya existe un usuario con el mail '{mail}'")
        usuario = Usuario(nombre, apellido, mail, celular, contrasenia, rol)
        self.__usuarios.append(usuario)
        return usuario

    def editar(
        self,
        id_usuario: int,
        nombre: Optional[str] = None,
        apellido: Optional[str] = None,
        mail: Optional[str] = None,
        celular: Optional[str] = None,
        contrasenia: Optional[str] = None,
        rol: Optional[Rol] = None,
    ) -> Usuario:
        usuario = self.buscar_por_id(id_usuario)
        if nombre is not None and nombre.strip():
            usuario.nombre = nombre
        if apellido is not None and apellido.strip():
            usuario.apellido = apellido
        if mail is not None and mail.strip():
            if self._existe_mail(mail, excluir_id=id_usuario):
                raise DuplicadoError(f"Ya existe un usuario con el mail '{mail}'")
            usuario.mail = mail
        if celular is not None and celular.strip():
            usuario.celular = celular
        if contrasenia is not None and contrasenia.strip():
            usuario.contrasenia = contrasenia
        if rol is not None:
            usuario.rol = rol
        return usuario

    def eliminar(self, id_usuario: int, usuario_sesion: Usuario) -> None:
        usuario = self.buscar_por_id(id_usuario)
        if usuario.id == usuario_sesion.id:
            raise OperacionNoPermitidaError(
                "Un administrador no puede eliminarse a sí mismo mientras tiene la sesión iniciada"
            )
        usuario.eliminado = True

    def autenticar(self, mail: str, contrasenia: str) -> Usuario:
        """Autentica y devuelve el usuario. Siempre el mismo mensaje de error."""
        usuario = self.buscar_por_mail(mail, solo_activos=True)
        if usuario is None or not usuario.verificar_contrasenia(contrasenia):
            raise CredencialesInvalidasError("Mail o contraseña incorrectos")
        return usuario
