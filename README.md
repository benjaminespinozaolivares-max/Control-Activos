# CONTROL-ACTIVOS

### Sistema de gestión y trazabilidad de activos físicos

**CONTROL-ACTIVOS** es una aplicación de escritorio desarrollada en
Python para gestionar y mantener la trazabilidad de los movimientos de
activos físicos mediante operaciones de solicitud y devolución.

El sistema permite registrar quién solicita un activo, qué elemento se
entrega, qué operador registra la operación y cuándo se realiza el
movimiento. También incorpora herramientas para consultar el historial y
exportar los registros.

------------------------------------------------------------------------

## Objetivo del proyecto

Desarrollar una herramienta que centralice el registro de entregas y
devoluciones de activos físicos, facilite la consulta de operaciones
anteriores y permita identificar a los participantes de cada movimiento.

## Funcionalidades

-   **Autenticación de usuarios:** acceso mediante RUT y contraseña, con
    verificación de contraseñas mediante Argon2id.
-   **Registro de solicitudes:** registra la entrega de un activo e
    identifica al solicitante y al operador responsable.
-   **Registro de devoluciones:** permite localizar una solicitud
    pendiente y registrar la devolución del activo.
-   **Consulta de registros:** muestra el historial de solicitudes y
    devoluciones.
-   **Búsqueda:** permite filtrar los registros disponibles.
-   **Exportación a Excel:** genera archivos `.xlsx` con la información
    consultada.

## Tecnologías utilizadas

  Tecnología      Uso
  --------------- -----------------------------------------------
  Python          Lenguaje principal del proyecto
  Tkinter / ttk   Interfaz gráfica de escritorio
  SQLite          Almacenamiento de datos
  Pandas          Conversión y procesamiento de registros
  OpenPyXL        Escritura de archivos Excel
  Argon2-cffi     Generación y verificación de hashes Argon2id
  Git / GitHub    Control de versiones y alojamiento del código

## Estructura del proyecto

``` text
CONTROL-ACTIVOS/
│
├── main.py
├── login.py
├── assets_log.py
├── ope_action.py
├── search_sql.py
├── register.py
├── tables_sql.py
├── hash_coder_user.py
│
├── README.md
└── .gitignore
```

### Responsabilidad de los módulos

-   `main.py`: inicia la aplicación y coordina la transición entre el
    inicio de sesión y la interfaz principal.
-   `login.py`: contiene la interfaz de acceso y la lógica de
    autenticación.
-   `assets_log.py`: contiene la interfaz gráfica principal y las vistas
    de operación, consulta y búsqueda.
-   `ope_action.py`: implementa la lógica de las operaciones de
    solicitud y devolución.
-   `search_sql.py`: contiene las consultas SQL, la recuperación de
    registros y la exportación a Excel.
-   `register.py`: contiene las operaciones de inserción y actualización
    de datos.
-   `tables_sql.py`: establece la conexión con la base de datos
    operacional y crea sus tablas.
-   `hash_coder_user.py`: herramienta auxiliar para generar hashes
    Argon2id destinados al registro manual de usuarios autorizados.

## Bases de datos

La aplicación utiliza dos bases de datos SQLite independientes:

### `auth_beta.db`

Almacena los datos de los usuarios autorizados para ingresar al sistema,
incluyendo sus identificadores, RUT, información de perfil, rol y hash
de contraseña.

Las contraseñas se almacenan como hashes Argon2id. *La creación de
cuentas administrativas se realiza manualmente y no está disponible como
función de la interfaz de la aplicación.*

### `tables_beta.db`

Almacena la información operacional del sistema mediante las siguientes
tablas:

-   `usuarios`: datos de los operadores.
-   `personal`: datos de las personas que solicitan activos.
-   `activo`: información de los activos registrados.
-   `registro_general`: historial de solicitudes y devoluciones.

La tabla `registro_general` almacena los identificadores asociados al
operador, al solicitante y al activo, además de la fecha y las horas de
entrega y devolución.

## Instalación y ejecución

### Requisitos

-   Python 3.10 o superior.
-   Pip.
-   Windows (entorno de desarrollo previsto).

### 1. Clonar el repositorio

``` bash
git clone URL_DEL_REPOSITORIO
```

### 2. Entrar en el directorio del proyecto

``` bash
cd CONTROL-ACTIVOS
```

### 3. Instalar las dependencias

``` bash
python -m pip install pandas openpyxl argon2-cffi
```

### 4. Ejecutar la aplicación

``` bash
python main.py
```

Para utilizar la aplicación se deben disponer de usuarios autorizados y
de los datos operacionales necesarios en las bases de datos
correspondientes.

## Seguridad y manejo de datos

-   Las contraseñas se almacenan mediante hashes Argon2id, no como texto
    plano.
-   La autenticación se mantiene separada de los datos operacionales.
-   La creación de usuarios administrativos se realiza fuera de la
    interfaz principal.
-   Las bases de datos que contengan credenciales, hashes o información
    personal real no deben publicarse en repositorios públicos.

## Estado del proyecto

**CONTROL-ACTIVOS** se encuentra en la etapa de cierre de su MVP
(*Minimum Viable Product*).

Esta primera versión busca entregar un flujo funcional para autenticar
operadores, registrar solicitudes y devoluciones, consultar el historial
y exportar los registros.

Las futuras modificaciones se realizarán cuando exista una necesidad
operativa, una corrección necesaria o una decisión explícita de ampliar
el alcance del proyecto.

## Autor

Proyecto personal desarrollado por Benjamín Espinoza O. Como parte del aprendizaje y aplicación
práctica de programación, bases de datos relacionales y desarrollo de
aplicaciones de escritorio.

------------------------------------------------------------------------

**CONTROL-ACTIVOS --- Gestión y trazabilidad de activos físicos.**
