from argon2 import PasswordHasher

def crear_hash():
    insertar_contraseña = input("*considere Mayusculas, números y caracteres especiales* Ingresa la nueva contraseña:       ")
    ph = PasswordHasher()
    hash_password = ph.hash(insertar_contraseña)

    # Verificar contraseña
    ph.verify(hash_password, insertar_contraseña)
    print(hash_password)

def start():
    while(1):
        crear_hash()

start()