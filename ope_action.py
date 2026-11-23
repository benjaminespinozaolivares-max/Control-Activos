import search_sql
import register
from datetime import datetime

def nueva_solicitud(qr_personal, rut_usuario, codigo_activo):

    tiempo = datetime.now()
    fecha = tiempo.strftime("%d/%m/%Y")
    hora = tiempo.strftime("%H:%M")

    rut_solicitante = search_sql.patron_rut_personal(qr_personal)

    id_personal = search_sql.buscar_id_personal(rut_solicitante)
    id_usuario = search_sql.buscar_id_usuario(rut_usuario)
    id_activo = search_sql.buscar_id_activo(codigo_activo)

    fecha_registro = fecha
    hora_entrega = hora

    register.registrar_solicitud(
        id_usuario,
        id_personal,
        id_activo,
        fecha_registro,
        hora_entrega
    )

    return True

def nueva_devolucion(qr_personal, codigo_activo):

    rut_solicitante = search_sql.patron_rut_personal(qr_personal)

    id_personal = search_sql.buscar_id_personal(rut_solicitante)

    id_activo = search_sql.buscar_id_activo(codigo_activo)

    tiempo = datetime.now()
    hora = tiempo.strftime("%H:%M")

    registro_resultado = search_sql.buscar_registro_inconcluso(
        id_activo,
        id_personal
    )

    if registro_resultado is not None:

        register.terminar_registro(
            hora,
            int(registro_resultado)
        )

        return True

    else:

        return False

# código sin cambios.
