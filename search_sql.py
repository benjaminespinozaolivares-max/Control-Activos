import tables_sql
import re
import pandas as pd

conexion_db = tables_sql.conn
cursor = conexion_db.cursor()

def buscar_id_personal(rut_personal):
    cursor.execute("""
    SELECT id_personal FROM personal 
    WHERE rut_personal = ?
    """, (rut_personal,))

    resultado = cursor.fetchone()
    if resultado is not None:
            return resultado[0]
    else:
            return None


def buscar_id_usuario(rut_usuario):
    cursor.execute("""
    SELECT id_usuario FROM usuarios
    WHERE rut_usuario = ?
    """, (rut_usuario,))

    resultado = cursor.fetchone()
    tupla = resultado[0]
    if resultado is not None:
            return resultado[0]
    else:
            return None


def buscar_id_activo(codigo_activo):
    cursor.execute("""
    SELECT id_activo FROM activo
    WHERE codigo_activo = ?
    """, (codigo_activo,))

    resultado = cursor.fetchone()
    tupla = resultado[0]
    if resultado is not None:
            return resultado[0]
    else:
            return None


def buscar_registro_inconcluso(id_activo, id_personal):

    cursor.execute("""
    SELECT id_solicitud FROM registro_general
    WHERE id_activo_reg = ?
    AND id_personal_reg = ?
    AND hora_devolucion_reg IS NULL
    """, (id_activo, id_personal))

    resultado = cursor.fetchone()

    if resultado is not None:
        return resultado[0]

    else:
        return None

def patron_rut_usuario(qr_scan_usuario):

    patron_resultado = re.search(r"\d{7,8}-[\dkK]", qr_scan_usuario)
    rut_string = patron_resultado.group()
    return rut_string
    # esta función utiliza el patrón para buscar el rut dentro de los URL de los QR de las cédulas

def patron_rut_personal(qr_scan_personal):

    patron_resultado = re.search(r"\d{7,8}-[\dkK]", qr_scan_personal)
    rut_string = patron_resultado.group()
    return rut_string
    # esta función utiliza el patrón para buscar el rut dentro de los URL de los QR de las cédulas

def mostrar_registros():
    cursor.execute("""
    SELECT fecha_reg,
    nombre_activo, articulo_activo,
    nombre_personal, apellido_personal, empresa_personal,
    nombre_usuario, apellido_usuario, empresa_usuario,
    hora_entrega_reg, hora_devolucion_reg
    FROM registro_general
    INNER JOIN activo
    ON activo.id_activo = registro_general.id_activo_reg
    INNER JOIN personal
    ON personal.id_personal = registro_general.id_personal_reg
    INNER JOIN usuarios
    ON usuarios.id_usuario = registro_general.id_usuario_reg
    
    """)
    resultados_registros = cursor.fetchall()
    return resultados_registros

def export_registros_excel():
    columnas = [
        "Fecha",
        "Activo",
        "Tipo de activo",
        "Nombre solicitante",
        "Apellido solicitante",
        "Empresa solicitante",
        "Nombre operador",
        "Apellido operador",
        "Empresa operador",
        "Hora entrega",
        "Hora devolución"
    ]

    df = pd.DataFrame(mostrar_registros(), columns=columnas)
    df.to_excel("registros_control_activos.xlsx", index=False)


# Sin necesidad de modificaciones