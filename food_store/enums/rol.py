from enum import Enum


class Rol(Enum):
    ADMIN = "ADMIN"
    USUARIO = "USUARIO"

    def __str__(self) -> str:
        return self.value
