import tables_sql
from datetime import datetime

conexion_db = tables_sql.conn
cursor = conexion_db.cursor()

def registrar_activo(
        nombre_activo,
        articulo_activo,
        numero_activo,
        codigo_activo
):
    cursor.execute("""
    INSERT INTO activo (
    nombre_activo,
    articulo_activo,
    numero-activo,
    codigo_activo
    ) VALUES (?, ?, ?, ?)
    """, (nombre_activo, articulo_activo, numero_activo, codigo_activo))
    conexion_db.commit()
    return True

def registrar_personal(
        nombre_personal,
        apellido_personal,
        rut_personal,
        empresa_personal,
        cargo_personal
):
    cursor.execute("""
    INSERT INTO personal (
    nombre_personal,
    apellido_personal,
    rut_personal,
    empresa_personal,
    cargo_personal
    ) VALUES (?, ?, ?, ?, ?)
    """, (nombre_personal, apellido_personal, rut_personal, empresa_personal, cargo_personal))
    conexion_db.commit()
    return True

def registrar_usuario(
        nombre_usuario,
        apellido_usuario,
        rut_usuario,
        empresa_usuario,
        contrasena_usuario
):
    cursor.execute("""
    INSERT INTO usuarios (
    nombre_usuario,
    apellido_usuario,
    rut_usuario,
    empresa_usuario,
    contrasena_usuario
    ) VALUES (?, ?, ?, ?, ?)
    """, (nombre_usuario, apellido_usuario, rut_usuario, empresa_usuario, contrasena_usuario))
    conexion_db.commit()
    return True

def registrar_solicitud(
        id_usuario_reg,
        id_personal_reg,
        id_activo_reg,
        fecha_reg,
        hora_entrega_reg

):
    cursor.execute("""
    INSERT INTO registro_general (
        id_usuario_reg,
        id_personal_reg,
        id_activo_reg,
        fecha_reg,
        hora_entrega_reg
    ) VALUES (?, ?, ?, ?, ?)
    """, (id_usuario_reg, id_personal_reg, id_activo_reg, fecha_reg, hora_entrega_reg,))
    conexion_db.commit()
    return True

tiempo = datetime.now()
hora = tiempo.strftime("%H:%M")


def terminar_registro(
    hora_devolucion_reg,
    id_solicitud
):
    cursor.execute("""
    UPDATE registro_general 
    SET hora_devolucion_reg = ?
    WHERE id_solicitud = ?
    AND hora_devolucion_reg IS NULL
    
    """, (hora_devolucion_reg, id_solicitud,))
    conexion_db.commit()
    return True


# sin necesidad de modificaciones