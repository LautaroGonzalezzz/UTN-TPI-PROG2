from entidades.base import Base
from enums import Rol
from excepciones import DatoInvalidoError


class Usuario(Base):
    """Representa un usuario del sistema (administrador o cliente)."""

    def __init__(
        self,
        nombre: str,
        apellido: str,
        mail: str,
        celular: str,
        contrasenia: str,
        rol: Rol,
    ) -> None:
        super().__init__()
        self.nombre = nombre
        self.apellido = apellido
        self.mail = mail
        self.celular = celular
        self.__contrasenia: str = ""
        self.contrasenia = contrasenia  # usa el setter
        self.rol = rol

    @property
    def nombre(self) -> str:
        return self.__nombre

    @nombre.setter
    def nombre(self, valor: str) -> None:
        if not valor or not valor.strip():
            raise DatoInvalidoError("El nombre no puede estar vacío")
        self.__nombre = valor.strip()

    @property
    def apellido(self) -> str:
        return self.__apellido

    @apellido.setter
    def apellido(self, valor: str) -> None:
        if not valor or not valor.strip():
            raise DatoInvalidoError("El apellido no puede estar vacío")
        self.__apellido = valor.strip()

    @property
    def mail(self) -> str:
        return self.__mail

    @mail.setter
    def mail(self, valor: str) -> None:
        if not valor or not valor.strip():
            raise DatoInvalidoError("El mail no puede estar vacío")
        valor = valor.strip().lower()
        if "@" not in valor or "." not in valor:
            raise DatoInvalidoError("El mail debe tener un formato válido (contener @ y .)")
        self.__mail = valor

    @property
    def celular(self) -> str:
        return self.__celular

    @celular.setter
    def celular(self, valor: str) -> None:
        if not valor or not valor.strip():
            raise DatoInvalidoError("El celular no puede estar vacío")
        self.__celular = valor.strip()

    # Sin property de lectura para la contraseña
    @property
    def contrasenia(self) -> None:
        raise AttributeError("La contraseña no se puede leer")

    @contrasenia.setter
    def contrasenia(self, valor: str) -> None:
        if not valor or not valor.strip():
            raise DatoInvalidoError("La contraseña no puede estar vacía")
        self.__contrasenia = valor

    def verificar_contrasenia(self, contrasenia: str) -> bool:
        """Compara la contraseña recibida con la almacenada sin exponerla."""
        return self.__contrasenia == contrasenia

    @property
    def rol(self) -> Rol:
        return self.__rol

    @rol.setter
    def rol(self, valor: Rol) -> None:
        if not isinstance(valor, Rol):
            raise DatoInvalidoError("El rol debe ser un valor de Rol")
        self.__rol = valor

    def nombre_completo(self) -> str:
        return f"{self.nombre} {self.apellido}"

    def __str__(self) -> str:
        return f"[{self.id}] {self.nombre_completo()} | {self.mail} | {self.rol}"
