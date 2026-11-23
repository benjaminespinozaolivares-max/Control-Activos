import sqlite3

conn = sqlite3.connect('tables_beta.db')
cursor = conn.cursor()
# CREAR TABLAS #
##############   USUARIOS   ###########################
cursor.execute('''
CREATE TABLE IF NOT EXISTS usuarios (
id_usuario INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
nombre_usuario TEXT NOT NULL,
apellido_usuario TEXT NOT NULL,
rut_usuario TEXT NOT NULL UNIQUE,
empresa_usuario TEXT,
contrasena_usuario TEXT NOT NULL
)
''')
#############   PERSONAL    ###########################
cursor.execute('''
CREATE TABLE IF NOT EXISTS personal (
id_personal INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
nombre_personal TEXT NOT NULL,
apellido_personal TEXT NOT NULL,
rut_personal TEXT NOT NULL UNIQUE,
empresa_personal TEXT,
cargo_personal TEXT 
)
''')
############    ACTIVO  ###############################
cursor.execute('''
CREATE TABLE IF NOT EXISTS activo (
id_activo INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
nombre_activo TEXT NOT NULL,
articulo_activo TEXT NOT NULL,
numero_activo INTEGER,
codigo_activo TEXT NOT NULL UNIQUE
)
''')
##########      REGISTRO GENERAL    ###################
cursor.execute('''
CREATE TABLE IF NOT EXISTS registro_general (
id_solicitud INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
id_usuario_reg INTEGER NOT NULL,
id_personal_reg INTEGER NOT NULL,
id_activo_reg INTEGER NOT NULL,
fecha_reg DATE NOT NULL,
hora_entrega_reg TIME,
hora_devolucion_reg TIME
)
''')
###############     FIN CREAR TABLAS    #####################
conn.commit()
# Archivo sin necesidad de modificaciones.