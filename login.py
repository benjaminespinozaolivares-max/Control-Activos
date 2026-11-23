import tkinter as tk
from tkinter import ttk
import sqlite3
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError, VerificationError
from pathlib import Path

# CONEXIÓN A LA BASE DE DATOS Y CREACIÓN DE LA TABLA DE USUARIOS...
conexion_sql_db = sqlite3.connect('auth_beta.db')
cursor_login_sql = conexion_sql_db.cursor()

cursor_login_sql.execute('''
    CREATE TABLE IF NOT EXISTS program_users
    (
        Id
        INTEGER
        NOT
        NULL
        PRIMARY
        KEY
        AUTOINCREMENT,
        NOMBRE
        TEXT
        NOT
        NULL,
        APELLIDO
        TEXT
        NOT
        NULL,
        RUT
        TEXT
        NOT
        NULL
        UNIQUE,
        EMPRESA
        TEXT
        NOT
        NULL,
        CARGO
        TEXT
        NOT
        NULL,
        PASSWORD
        TEXT
        NOT
        NULL
        UNIQUE,
        ROL
        TEXT
        NOT
        NULL
    )''')
conexion_sql_db.commit()
conexion_sql_db.close()


def autenticar_usuario(rut, password):

    ruta_db = Path(__file__).resolve().parent / "auth_beta.db"

    if not rut or not password:
        return False

    rut = rut.strip().replace(".", "").upper()

    try:
        conexion = sqlite3.connect(ruta_db)
        cursor = conexion.cursor()

        cursor.execute("""
            SELECT PASSWORD
            FROM program_users
            WHERE UPPER(REPLACE(RUT, '.', '')) = ?
        """, (rut,))

        resultado = cursor.fetchone()
        conexion.close()

        if resultado is None:
            return False

        password_hash = resultado[0]

        ph = PasswordHasher()

        return ph.verify(password_hash, password)

    except (VerifyMismatchError, VerificationError):
        return False

    except sqlite3.Error:
        return False


# BLOQUE DE CODIGO PARA LA INTERFAZ DE USUARIO Y LOGIN

class LoginApp:
    # Paleta de colores
    BG = "#11161D"
    PANEL = "#202A36"
    SIDEBAR = "#171F29"
    BORDER = "#344252"
    TEXT = "#E8EDF3"
    MUTED = "#9AA8B7"
    ACCENT = "#F2A900"
    ACCENT_HOVER = "#FFC233"
    RED = "#FF5555"

    def __init__(self, root, on_success):
        self.root = root
        self.on_success = on_success

        self.root.title("CONTROL-ACTIVOS | Acceso")
        self.root.geometry("900x560")
        self.root.resizable(False, False)
        self.root.configure(bg=self.BG)

        self.configurar_estilos()
        self.crear_interfaz()

    def configurar_estilos(self):
        self.style = ttk.Style()
        self.style.theme_use("clam")

        self.style.configure(
            "TEntry",
            fieldbackground="#151C25",
            foreground=self.TEXT,
            insertcolor=self.TEXT,
            bordercolor=self.BORDER,
            padding=12
        )

        self.style.configure(
            "Login.TButton",
            background=self.ACCENT,
            foreground="#15191F",
            font=("Segoe UI", 10, "bold"),
            padding=(15, 12),
            borderwidth=0
        )

        self.style.map(
            "Login.TButton",
            background=[
                ("active", self.ACCENT_HOVER),
                ("pressed", "#D18F00")
            ]
        )

    def crear_interfaz(self):
        contenedor = tk.Frame(self.root, bg=self.BG)
        contenedor.pack(fill="both", expand=True)
        contenedor.columnconfigure(0, weight=1)
        contenedor.columnconfigure(1, weight=1)
        contenedor.rowconfigure(0, weight=1)

        # PANEL IZQUIERDO
        panel_izquierdo = tk.Frame(contenedor, bg=self.SIDEBAR)
        panel_izquierdo.grid(row=0, column=0, sticky="nsew")

        tk.Label(
            panel_izquierdo,
            text="CA",
            bg=self.ACCENT,
            fg="#15191F",
            font=("Segoe UI", 30, "bold"),
            width=3,
            height=1
        ).pack(anchor="w", padx=45, pady=(100, 20))

        tk.Label(
            panel_izquierdo,
            text="CONTROL-ACTIVOS",
            bg=self.SIDEBAR,
            fg=self.TEXT,
            font=("Segoe UI", 20, "bold")
        ).pack(anchor="w", padx=45)

        tk.Label(
            panel_izquierdo,
            text="GESTIÓN Y TRAZABILIDAD",
            bg=self.SIDEBAR,
            fg=self.ACCENT,
            font=("Segoe UI", 9, "bold")
        ).pack(anchor="w", padx=45, pady=(8, 35))

        tk.Frame(
            panel_izquierdo,
            bg=self.BORDER,
            height=2,
            width=65
        ).pack(anchor="w", padx=45)

        # PANEL DERECHO
        panel_derecho = tk.Frame(contenedor, bg=self.BG, padx=55)
        panel_derecho.grid(row=0, column=1, sticky="nsew")
        panel_derecho.columnconfigure(0, weight=1)

        tk.Label(
            panel_derecho,
            text="BIENVENIDO",
            bg=self.BG,
            fg=self.TEXT,
            font=("Segoe UI", 23, "bold")
        ).grid(row=0, column=0, sticky="w", pady=(105, 5))

        tk.Label(
            panel_derecho,
            text="Ingresa tus credenciales para continuar.",
            bg=self.BG,
            fg=self.MUTED,
            font=("Segoe UI", 9)
        ).grid(row=1, column=0, sticky="w", pady=(0, 35))

        # CAMPO RUT
        tk.Label(
            panel_derecho,
            text="RUT/DNI DEL OPERADOR",
            bg=self.BG,
            fg=self.MUTED,
            font=("Segoe UI", 8, "bold")
        ).grid(row=2, column=0, sticky="w", pady=(0, 8))

        self.rut_entry = ttk.Entry(panel_derecho, font=("Segoe UI", 10))
        self.rut_entry.grid(
            row=3, column=0, sticky="ew", ipady=3, pady=(0, 22)
        )

        # CAMPO CONTRASEÑA
        tk.Label(
            panel_derecho,
            text="CONTRASEÑA",
            bg=self.BG,
            fg=self.MUTED,
            font=("Segoe UI", 8, "bold")
        ).grid(row=4, column=0, sticky="w", pady=(0, 8))

        self.password_entry = ttk.Entry(
            panel_derecho,
            show="*",
            font=("Segoe UI", 10)
        )
        self.password_entry.grid(
            row=5, column=0, sticky="ew", ipady=3, pady=(0, 30)
        )

        # BOTÓN LOGIN
        ttk.Button(
            panel_derecho,
            text="INICIAR SESIÓN   →",
            style="Login.TButton",
            command=self.iniciar_sesion
        ).grid(row=6, column=0, sticky="ew", ipady=3)


        self.rut_entry.focus_set()
        self.password_entry.bind(
            "<Return>",
            lambda event: self.iniciar_sesion()
        )

    def iniciar_sesion(self):

        rut = self.rut_entry.get().strip()
        password = self.password_entry.get()

        if not rut or not password:
            self.mensaje_label.configure(
                text="Debes ingresar RUT y contraseña.",
                fg=self.RED
            )

            return

        autenticado = autenticar_usuario(rut, password)

        if autenticado:

            rut_usuario = rut.strip().replace(".", "").upper()
            self.on_success(rut_usuario)

        else:

            self.mensaje_label.configure(
                text="RUT o contraseña incorrectos.",
                fg=self.RED
            )

            self.password_entry.delete(0, tk.END)
            self.password_entry.focus_set()
# FIN CÓDIGO...