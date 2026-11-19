# Food Store – Sistema de Gestión de Pedidos de Comida (Consola)

Aplicación de consola orientada a objetos en Python 3.12+ para gestionar categorías, productos, usuarios y pedidos de un negocio de comidas.

## Requisitos

- Python 3.12 o superior
- Solo biblioteca estándar (`abc`, `enum`, `datetime`, `getpass`)
- Sin instalación de paquetes externos

## Cómo ejecutar

```bash
cd food_store
python main.py
```

### Credenciales iniciales

| Rol     | Mail                  | Contraseña  |
|---------|-----------------------|-------------|
| ADMIN   | admin@foodstore.com   | admin123    |
| USUARIO | juan@cliente.com      | cliente123  |

## Pruebas del modelo y servicios

```bash
python pruebas.py
```

## Enlaces de la entrega

- Video demostración: https://youtu.be/E2KyS0OnTaM?si=Om-i51dKi3JijyD1
- Informe PDF: file:///C:/Users/latip/Documents/UTN/Segundo%20Semestre/Programacion%20II/TPI/Food_Store_TPI.pdf
  
## Estructura del proyecto

```
food_store/
├── main.py                 # Punto de entrada (crea servicios y corre login → menú)
├── datos_iniciales.py      # Administrador inicial y datos de ejemplo
├── formato.py              # Formato de pesos y fechas
├── pruebas.py              # Pruebas unitarias del modelo y servicios
├── entidades/              # Clases del UML (Base, Categoria, Producto, ...)
├── enums/                  # Rol, Estado, FormaPago
├── excepciones/            # FoodStoreError y subclases
├── servicios/              # Lógica de negocio y colecciones
└── consola/                # Menús polimórficos, login, estilos de terminal, tablas y lectura validada
```

## Interfaz de consola

- Menús con flechas ↑ ↓ y Enter, o pulsando directamente el número de la opción.
- Colores, banner, tablas y mensajes ✔ / ✖ con solo la biblioteca estándar.
- Si la salida no es una terminal (o está definida `NO_COLOR`) se muestra texto plano y menú numérico.
- Funciona en Windows 10+ (cmd, PowerShell, terminal de VS Code), Linux y macOS.

## Características principales

- **POO**: herencia desde clase abstracta `Base`, interfaz `Calculable`, composición en `Pedido`–`DetallePedido`, encapsulamiento con `@property`.
- **Roles**: menú resuelto por polimorfismo (`MenuAdministrador` / `MenuCliente`).
- **Validaciones y excepciones propias**: `EntidadNoEncontradaError`, `StockInsuficienteError`, `DuplicadoError`, etc.
- **Baja lógica**: `eliminado = True`; los datos no se borran de la colección.
- **Type hints** en todos los atributos, parámetros y retornos.

## Arquitectura

```
consola → servicios → entidades
```

La consola solo pide datos y muestra mensajes; los servicios aplican reglas de negocio; las entidades validan su propio estado.
