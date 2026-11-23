import tkinter as tk
from tkinter import ttk, messagebox
import search_sql
import ope_action


class ControlActivosApp:

    # ---------------------------------
    # PALETA INDUSTRIAL / DARK
    # ---------------------------------

    BG = "#11161D"
    SIDEBAR = "#171F29"
    PANEL = "#202A36"
    PANEL_ALT = "#263341"
    BORDER = "#344252"
    TEXT = "#E8EDF3"
    MUTED = "#9AA8B7"
    ACCENT = "#F2A900"
    ACCENT_HOVER = "#FFC233"
    GREEN = "#36B37E"
    RED = "#E05D5D"

    def __init__(self, root, rut_usuario=None):
        self.root = root
        self.rut_usuario = rut_usuario
        self.root.title("CONTROL-ACTIVOS | Sistema de trazabilidad")
        self.root.geometry("1240x780")
        self.root.minsize(1050, 680)
        self.root.configure(bg=self.BG)
        self.root.option_add("*tearOff", False)
        self.registros_cache = []
        self.vista_actual = None

        self.style = ttk.Style()
        self.configurar_estilos()

        self.crear_layout()
        self.root.bind("<Control-r>", lambda event: self.refrescar_vista())
        self.root.bind("<Escape>", lambda event: self.limpiar_busqueda())
        self.mostrar_inicio()

    # ---------------------------------
    # CONFIGURACIÓN VISUAL
    # ---------------------------------

    def configurar_estilos(self):

        self.style.theme_use("clam")

        self.style.configure(
            ".",
            font=("Segoe UI", 10),
            background=self.BG,
            foreground=self.TEXT
        )

        self.style.configure(
            "TFrame",
            background=self.BG
        )

        self.style.configure(
            "Sidebar.TFrame",
            background=self.SIDEBAR
        )

        self.style.configure(
            "Panel.TFrame",
            background=self.PANEL
        )

        self.style.configure(
            "Title.TLabel",
            background=self.BG,
            foreground=self.TEXT,
            font=("Segoe UI", 23, "bold")
        )

        self.style.configure(
            "Subtitle.TLabel",
            background=self.BG,
            foreground=self.MUTED,
            font=("Segoe UI", 10)
        )

        self.style.configure(
            "Section.TLabel",
            background=self.PANEL,
            foreground=self.TEXT,
            font=("Segoe UI", 12, "bold")
        )

        self.style.configure(
            "Field.TLabel",
            background=self.PANEL,
            foreground=self.MUTED,
            font=("Segoe UI", 9, "bold")
        )

        self.style.configure(
            "TEntry",
            fieldbackground="#151C25",
            foreground=self.TEXT,
            insertcolor=self.TEXT,
            bordercolor=self.BORDER,
            lightcolor=self.BORDER,
            darkcolor=self.BORDER,
            padding=10
        )

        self.style.map(
            "TEntry",
            bordercolor=[("focus", self.ACCENT)]
        )

        self.style.configure(
            "Primary.TButton",
            background=self.ACCENT,
            foreground="#15191F",
            font=("Segoe UI", 10, "bold"),
            padding=(18, 11),
            borderwidth=0,
            cursor="hand2"
        )

        self.style.map(
            "Primary.TButton",
            background=[
                ("pressed", "#D18F00"),
                ("active", self.ACCENT_HOVER)
            ],
            foreground=[("disabled", "#777777")]
        )

        self.style.configure(
            "Nav.TButton",
            background=self.SIDEBAR,
            foreground="#C2CCD6",
            font=("Segoe UI", 10, "bold"),
            anchor="w",
            padding=(15, 12),
            borderwidth=0,
            cursor="hand2"
        )

        self.style.map(
            "Nav.TButton",
            background=[
                ("pressed", self.PANEL_ALT),
                ("active", self.PANEL_ALT)
            ],
            foreground=[("active", self.ACCENT_HOVER)]
        )

        self.style.configure(
            "Export.TButton",
            background="#36B37E",
            foreground="#FFFFFF",
            font=("Segoe UI", 10, "bold"),
            padding=(18, 11),
            borderwidth=0,
            cursor="hand2"
        )

        self.style.map(
            "Export.TButton",
            background=[
                ("pressed", "#25865C"),
                ("active", "#45C990")
            ],
            foreground=[
                ("disabled", "#777777")
            ]
        )

        self.style.configure(
            "Treeview",
            background="#19222D",
            fieldbackground="#19222D",
            foreground=self.TEXT,
            rowheight=34,
            borderwidth=0,
            font=("Segoe UI", 9)
        )

        self.style.configure(
            "Treeview.Heading",
            background="#2B3948",
            foreground=self.ACCENT_HOVER,
            font=("Segoe UI", 9, "bold"),
            padding=(10, 12),
            relief="flat"
        )

        self.style.map(
            "Treeview",
            background=[("selected", "#66501D")],
            foreground=[("selected", "#FFFFFF")]
        )

        self.style.configure(
            "Vertical.TScrollbar",
            background=self.PANEL_ALT,
            troughcolor=self.BG,
            bordercolor=self.BG,
            arrowcolor=self.TEXT
        )

        self.style.configure(
            "Horizontal.TScrollbar",
            background=self.PANEL_ALT,
            troughcolor=self.BG,
            bordercolor=self.BG,
            arrowcolor=self.TEXT
        )

    # ---------------------------------
    # ESTRUCTURA PRINCIPAL
    # ---------------------------------

    def crear_layout(self):

        self.root.columnconfigure(1, weight=1)
        self.root.rowconfigure(0, weight=1)

        self.sidebar = ttk.Frame(
            self.root,
            style="Sidebar.TFrame",
            padding=(18, 22),
            width=245
        )
        self.sidebar.grid(
            row=0,
            column=0,
            sticky="ns"
        )
        self.sidebar.grid_propagate(False)

        self.main_shell = tk.Frame(
            self.root,
            bg=self.BG
        )
        self.main_shell.grid(
            row=0,
            column=1,
            sticky="nsew"
        )
        self.main_shell.rowconfigure(1, weight=1)
        self.main_shell.columnconfigure(0, weight=1)

        # Identidad visual
        tk.Label(
            self.sidebar,
            text="CA",
            bg=self.ACCENT,
            fg="#15191F",
            font=("Segoe UI", 19, "bold"),
            width=3,
            height=1
        ).pack(anchor="w", pady=(5, 12))

        tk.Label(
            self.sidebar,
            text="CONTROL-ACTIVOS",
            bg=self.SIDEBAR,
            fg=self.TEXT,
            font=("Segoe UI", 13, "bold")
        ).pack(anchor="w")

        tk.Label(
            self.sidebar,
            text="GESTIÓN Y TRAZABILIDAD",
            bg=self.SIDEBAR,
            fg=self.MUTED,
            font=("Segoe UI", 8, "bold")
        ).pack(anchor="w", pady=(3, 30))

        ttk.Button(
            self.sidebar,
            text="⌂   Inicio",
            style="Nav.TButton",
            command=self.mostrar_inicio
        ).pack(fill="x", pady=10)

        tk.Label(
            self.sidebar,
            text="OPERACIONES",
            bg=self.SIDEBAR,
            fg="#738294",
            font=("Segoe UI", 8, "bold")
        ).pack(anchor="w", pady=(0, 9))

        ttk.Button(
            self.sidebar,
            text="▣   Nueva solicitud",
            style="Nav.TButton",
            command=self.mostrar_solicitud
        ).pack(fill="x", pady=3)

        ttk.Button(
            self.sidebar,
            text="↩   Nueva devolución",
            style="Nav.TButton",
            command=self.mostrar_busqueda_devolucion
        ).pack(fill="x", pady=3)

        ttk.Button(
            self.sidebar,
            text="▤   Consultar registros",
            style="Nav.TButton",
            command=self.mostrar_registros
        ).pack(fill="x", pady=3)

        spacer = tk.Frame(self.sidebar, bg=self.SIDEBAR)
        spacer.pack(fill="both", expand=True)

        tk.Frame(
            self.sidebar,
            bg=self.BORDER,
            height=1
        ).pack(fill="x", pady=(10, 14))

        # Barra superior
        self.topbar = tk.Frame(
            self.main_shell,
            bg="#151C25",
            height=58
        )
        self.topbar.grid(
            row=0,
            column=0,
            sticky="ew"
        )
        self.topbar.grid_propagate(False)

        tk.Label(
            self.topbar,
            text="CENTRO DE CONTROL  /  ACTIVOS",
            bg="#151C25",
            fg=self.MUTED,
            font=("Segoe UI", 9, "bold")
        ).pack(side="left", padx=25, pady=19)


        self.main_frame = tk.Frame(
            self.main_shell,
            bg=self.BG,
            padx=30,
            pady=28
        )
        self.main_frame.grid(
            row=1,
            column=0,
            sticky="nsew"
        )
        self.main_frame.columnconfigure(0, weight=1)
        self.main_frame.rowconfigure(0, weight=1)

        self.statusbar = tk.Frame(
            self.main_shell,
            bg="#151C25",
            height=30
        )
        self.statusbar.grid(row=2, column=0, sticky="ew")
        self.statusbar.grid_propagate(False)

    # ---------------------------------
    # COMPONENTES VISUALES REUTILIZABLES
    # ---------------------------------

    def actualizar_estado(self, mensaje, color=None):
        if hasattr(self, "status_label"):
            self.status_label.configure(
                text=f"● {mensaje}",
                fg=color or self.GREEN
            )

    def refrescar_vista(self):
        if self.vista_actual == "registros":
            self.mostrar_registros()
        elif self.vista_actual == "inicio":
            self.mostrar_inicio()
        else:
            self.actualizar_estado("Vista actualizada")

    def limpiar_busqueda(self):
        if hasattr(self, "buscar_entry") and self.buscar_entry.winfo_exists():
            self.buscar_entry.delete(0, tk.END)
            self.aplicar_filtro_registros()
        return "break"

    def aplicar_filtro_registros(self):
        if not hasattr(self, "tree") or not self.tree.winfo_exists():
            return

        criterio = self.buscar_entry.get().strip().casefold() if hasattr(self, "buscar_entry") else ""
        self.tree.delete(*self.tree.get_children())

        coincidencias = 0
        for indice, registro in enumerate(self.registros_cache):
            texto_fila = " ".join("" if valor is None else str(valor) for valor in registro).casefold()
            if criterio in texto_fila:
                etiqueta = "even" if coincidencias % 2 == 0 else "odd"
                self.tree.insert("", "end", values=registro, tags=(etiqueta,))
                coincidencias += 1

        if criterio:
            self.actualizar_estado(f"{coincidencias} coincidencia(s) encontradas", self.ACCENT)
        else:
            self.actualizar_estado(f"{len(self.registros_cache)} registro(s) cargados")

    def limpiar_main(self):

        for widget in self.main_frame.winfo_children():
            widget.destroy()

    def crear_encabezado(self, titulo, descripcion):

        tk.Label(
            self.main_frame,
            text=titulo,
            bg=self.BG,
            fg=self.TEXT,
            font=("Segoe UI", 23, "bold")
        ).pack(anchor="w")

        tk.Label(
            self.main_frame,
            text=descripcion,
            bg=self.BG,
            fg=self.MUTED,
            font=("Segoe UI", 10)
        ).pack(anchor="w", pady=(5, 22))

    def crear_panel(self, parent=None):

        if parent is None:
            parent = self.main_frame

        panel = tk.Frame(
            parent,
            bg=self.PANEL,
            highlightthickness=1,
            highlightbackground=self.BORDER
        )
        return panel

    def crear_campo(self, parent, etiqueta, fila, variable_name, width=48):

        tk.Label(
            parent,
            text=etiqueta.upper(),
            bg=self.PANEL,
            fg=self.MUTED,
            font=("Segoe UI", 8, "bold")
        ).grid(
            row=fila,
            column=0,
            sticky="w",
            padx=22,
            pady=(15, 7)
        )

        entry = ttk.Entry(
            parent,
            width=width
        )
        entry.grid(
            row=fila,
            column=1,
            sticky="ew",
            padx=(10, 22),
            pady=(15, 7),
            ipady=2
        )

        setattr(self, variable_name, entry)
        return entry

    def crear_tarjeta_metrica(self, parent, titulo, valor, detalle, columna):

        tarjeta = tk.Frame(
            parent,
            bg=self.PANEL,
            highlightthickness=1,
            highlightbackground=self.BORDER
        )
        tarjeta.grid(
            row=0,
            column=columna,
            sticky="nsew",
            padx=(0 if columna == 0 else 8, 8),
            pady=5
        )

        tk.Label(
            tarjeta,
            text=titulo.upper(),
            bg=self.PANEL,
            fg=self.MUTED,
            font=("Segoe UI", 8, "bold")
        ).pack(anchor="w", padx=17, pady=(15, 5))

        tk.Label(
            tarjeta,
            text=str(valor),
            bg=self.PANEL,
            fg=self.ACCENT,
            font=("Segoe UI", 25, "bold")
        ).pack(anchor="w", padx=17)

        tk.Label(
            tarjeta,
            text=detalle,
            bg=self.PANEL,
            fg=self.MUTED,
            font=("Segoe UI", 8)
        ).pack(anchor="w", padx=17, pady=(2, 15))

    # ---------------------------------
    # VISTA DE INICIO
    # ---------------------------------

    def mostrar_inicio(self):

        self.vista_actual = "inicio"
        self.limpiar_main()

        self.crear_encabezado(
            "Panel de control",
            "Resumen general de la gestión y trazabilidad de activos."
        )

        try:
            registros = search_sql.mostrar_registros()
            total = len(registros)
            pendientes = sum(1 for registro in registros if registro[-1] is None)
            devueltos = total - pendientes
            activos = len(set(registro[1] for registro in registros))
        except Exception:
            total = pendientes = devueltos = activos = "—"

        metricas = tk.Frame(
            self.main_frame,
            bg=self.BG
        )
        metricas.pack(fill="x", pady=(0, 20))

        for columna in range(4):
            metricas.columnconfigure(columna, weight=1)

        self.crear_tarjeta_metrica(
            metricas, "Solicitudes", total,
            "Registros históricos", 0
        )
        self.crear_tarjeta_metrica(
            metricas, "Pendientes", pendientes,
            "Activos aún no devueltos", 1
        )
        self.crear_tarjeta_metrica(
            metricas, "Devueltos", devueltos,
            "Operaciones completadas", 2
        )
        self.crear_tarjeta_metrica(
            metricas, "Activos utilizados", activos,
            "Tipos/nombres presentes en registros", 3
        )

        panel = self.crear_panel()
        panel.pack(fill="x", pady=(5, 15))

        tk.Label(
            panel,
            text="MÓDULOS DE OPERACIÓN",
            bg=self.PANEL,
            fg=self.TEXT,
            font=("Segoe UI", 11, "bold")
        ).pack(anchor="w", padx=20, pady=(18, 5))

        tk.Label(
            panel,
            text="Selecciona una operación desde el menú lateral para comenzar.",
            bg=self.PANEL,
            fg=self.MUTED,
            font=("Segoe UI", 9)
        ).pack(anchor="w", padx=20, pady=(0, 18))


    # ---------------------------------
    # VISTA DE NUEVA SOLICITUD
    # ---------------------------------

    def mostrar_solicitud(self):

        self.vista_actual = "solicitud"
        self.limpiar_main()

        self.crear_encabezado(
            "Nueva solicitud",
            "Registra la entrega de una llave, credencial u otro activo."
        )

        formulario = self.crear_panel()
        formulario.pack(fill="x", pady=(5, 15))
        formulario.columnconfigure(1, weight=1)

        tk.Label(
            formulario,
            text="DATOS DE LA OPERACIÓN",
            bg=self.PANEL,
            fg=self.ACCENT,
            font=("Segoe UI", 9, "bold")
        ).grid(
            row=0,
            column=0,
            columnspan=2,
            sticky="w",
            padx=22,
            pady=(20, 5)
        )

        self.crear_campo(
            formulario,
            "QR de cédula del solicitante",
            1,
            "qr_solicitante"
        )

        self.crear_campo(
            formulario,
            "Código QR del activo",
            2,
            "qr_activo"
        )

        ttk.Button(
            formulario,
            text="REGISTRAR SOLICITUD   →",
            style="Primary.TButton",
            command=self.registrar_solicitud
        ).grid(
            row=3,
            column=1,
            sticky="e",
            padx=22,
            pady=(20, 22)
        )

    # ---------------------------------
    # VISTA DE BÚSQUEDA DE DEVOLUCIÓN
    # ---------------------------------

    def mostrar_busqueda_devolucion(self):

        self.vista_actual = "devolucion"
        self.limpiar_main()

        self.crear_encabezado(
            "Procesar devolución",
            "Localiza la solicitud pendiente y registra el retorno del activo."
        )

        formulario = self.crear_panel()
        formulario.pack(fill="x", pady=(5, 15))
        formulario.columnconfigure(1, weight=1)

        tk.Label(
            formulario,
            text="IDENTIFICACIÓN DE LA DEVOLUCIÓN",
            bg=self.PANEL,
            fg=self.ACCENT,
            font=("Segoe UI", 9, "bold")
        ).grid(
            row=0,
            column=0,
            columnspan=2,
            sticky="w",
            padx=22,
            pady=(20, 5)
        )

        self.crear_campo(
            formulario,
            "QR de cédula del solicitante",
            1,
            "qr_devolucion"
        )

        self.crear_campo(
            formulario,
            "Código del activo",
            2,
            "codigo_activo_devolucion"
        )

        ttk.Button(
            formulario,
            text="PROCESAR DEVOLUCIÓN   →",
            style="Primary.TButton",
            command=self.buscar_devolucion
        ).grid(
            row=3,
            column=1,
            sticky="e",
            padx=22,
            pady=(20, 22)
        )

        tk.Label(
            self.main_frame,
            text="La devolución solo se completará si existe una solicitud pendiente para esa persona y ese activo.",
            bg=self.BG,
            fg=self.MUTED,
            font=("Segoe UI", 9),
            wraplength=800,
            justify="left"
        ).pack(anchor="w", pady=8)

    # ---------------------------------
    # VISTA DE REGISTROS
    # ---------------------------------

    def mostrar_registros(self):

        self.vista_actual = "registros"
        self.limpiar_main()

        self.crear_encabezado(
            "Registros de actividad",
            "Consulta el historial de entregas y devoluciones registradas."
        )

        buscador = self.crear_panel()
        buscador.pack(fill="x", pady=(0, 12))

        tk.Label(
            buscador,
            text="BUSCAR EN REGISTROS",
            bg=self.PANEL,
            fg=self.MUTED,
            font=("Segoe UI", 8, "bold")
        ).pack(side="left", padx=(18, 10), pady=16)

        self.buscar_entry = ttk.Entry(
            buscador,
            width=35
        )
        self.buscar_entry.pack(side="left", padx=5, pady=12, fill="x", expand=True)
        self.buscar_entry.bind("<KeyRelease>", lambda event: self.aplicar_filtro_registros())
        self.buscar_entry.bind("<Return>", lambda event: self.aplicar_filtro_registros())

        ttk.Button(
            buscador,
            text="LIMPIAR",
            style="Nav.TButton",
            command=self.limpiar_busqueda
        ).pack(side="right", padx=(4, 12), pady=9)

        ttk.Button(
            buscador,
            text='EXPORTAR A EXCEL',
            style="Export.TButton",
            command=search_sql.export_registros_excel
        ).pack(side="right", padx=4, pady=9)

        ttk.Button(
            buscador,
            text="ACTUALIZAR",
            style="Primary.TButton",
            command=self.mostrar_registros
        ).pack(side="right", padx=4, pady=9)

        tabla_frame = tk.Frame(
            self.main_frame,
            bg=self.PANEL,
            highlightthickness=1,
            highlightbackground=self.BORDER
        )
        tabla_frame.pack(fill="both", expand=True, pady=5)
        tabla_frame.rowconfigure(0, weight=1)
        tabla_frame.columnconfigure(0, weight=1)

        columnas = (
            "fecha",
            "Activo",
            "Tipo de Activo",
            "Nombre de Solicitante",
            "Apellido de Solicitante",
            "Empresa de Solicitante",
            "Nombre de Operador",
            "Apellido de Operador",
            "Empresa de Operador",
            "Hora de Entrega",
            "Hora de Devolucion"
        )

        self.tree = ttk.Treeview(
            tabla_frame,
            columns=columnas,
            show="headings"
        )

        encabezados = {
            "fecha": "Fecha",
            "Activo": "Activo",
            "Tipo de Activo": "Tipo de activo",
            "Nombre de Solicitante": "Nombre",
            "Apellido de Solicitante": "Apellido",
            "Empresa de Solicitante": "Empresa solicitante",
            "Nombre de Operador": "Operador",
            "Apellido de Operador": "Apellido operador",
            "Empresa de Operador": "Empresa operador",
            "Hora de Entrega": "Hora entrega",
            "Hora de Devolucion": "Hora devolución"
        }

        anchos = {
            "fecha": 105,
            "Activo": 125,
            "Tipo de Activo": 125,
            "Nombre de Solicitante": 125,
            "Apellido de Solicitante": 125,
            "Empresa de Solicitante": 145,
            "Nombre de Operador": 125,
            "Apellido de Operador": 125,
            "Empresa de Operador": 145,
            "Hora de Entrega": 110,
            "Hora de Devolucion": 120
        }

        for columna, texto in encabezados.items():
            self.tree.heading(columna, text=texto)
            self.tree.column(
                columna,
                width=anchos[columna],
                minwidth=95,
                anchor="center",
                stretch=False
            )

        scrollbar_y = ttk.Scrollbar(
            tabla_frame,
            orient="vertical",
            command=self.tree.yview
        )

        scrollbar_x = ttk.Scrollbar(
            tabla_frame,
            orient="horizontal",
            command=self.tree.xview
        )

        self.tree.configure(
            yscrollcommand=scrollbar_y.set,
            xscrollcommand=scrollbar_x.set
        )

        self.tree.grid(
            row=0,
            column=0,
            sticky="nsew",
            padx=(10, 0),
            pady=(10, 0)
        )

        scrollbar_y.grid(
            row=0,
            column=1,
            sticky="ns",
            pady=(10, 0)
        )

        scrollbar_x.grid(
            row=1,
            column=0,
            sticky="ew",
            padx=(10, 0)
        )

        self.tree.tag_configure(
            "even",
            background="#19222D",
            foreground=self.TEXT
        )
        self.tree.tag_configure(
            "odd",
            background="#202B38",
            foreground=self.TEXT
        )

        try:
            self.registros_cache = search_sql.mostrar_registros() or []
            self.aplicar_filtro_registros()
        except Exception as error:
            self.registros_cache = []
            self.actualizar_estado("Error al cargar registros", self.RED)
            messagebox.showerror(
                "Error de consulta",
                f"No fue posible cargar el historial.\\n\\nDetalle: {error}"
            )

    # ---------------------------------
    # FUNCIONES DE NEGOCIO
    # ---------------------------------

    def registrar_solicitud(self):

        qr_personal = self.qr_solicitante.get().strip()
        codigo_activo = self.qr_activo.get().strip()
        rut_usuario = self.rut_usuario

        if not qr_personal or not codigo_activo:
            messagebox.showwarning(
                "Datos incompletos",
                "Completa el QR del solicitante y el código del activo."
            )
            self.actualizar_estado("Faltan datos por completar", self.RED)
            return

        try:
            resultado = ope_action.nueva_solicitud(
                qr_personal,
                rut_usuario,
                codigo_activo
            )
            if resultado is True:
                mensaje = "Solicitud registrada correctamente"
            elif resultado is False:
                mensaje = "No se pudo registrar la solicitud"
            elif resultado is None:
                mensaje = "RUN no existe en la base de datos"
            self.actualizar_estado(mensaje)
            messagebox.showinfo("Resultado de la solicitud", str(mensaje))
            print(resultado)
        except Exception as error:
            self.actualizar_estado("No se pudo procesar la solicitud", self.RED)
            messagebox.showerror(
                "Error al registrar",
                f"Ocurrió un problema al registrar la solicitud.\\n\\nDetalle: {error}"
            )

    def buscar_devolucion(self):

        qr_personal = self.qr_devolucion.get().strip()
        codigo_activo = self.codigo_activo_devolucion.get().strip()

        if not qr_personal or not codigo_activo:
            messagebox.showwarning(
                "Datos incompletos",
                "Completa el QR del solicitante y el código del activo."
            )
            self.actualizar_estado("Faltan datos por completar", self.RED)
            return

        try:
            resultado = ope_action.nueva_devolucion(
                qr_personal,
                codigo_activo
            )
            if resultado:
                mensaje = "Devolución Satisfactoria"
            else:
                mensaje = "No se pudo comepletar la devolución"
            self.actualizar_estado(mensaje, self.GREEN)
            messagebox.showinfo("Resultado de la devolución", str(mensaje))
            print(resultado)
        except Exception as error:
            self.actualizar_estado("No se pudo procesar la devolución", self.RED)
            messagebox.showerror(
                "Error al procesar",
                f"Ocurrió un problema al procesar la devolución.\\n\\nDetalle: {error}"
            )

    def buscar_registros(self):

        self.aplicar_filtro_registros()


# ---------------------------------
# EJECUCIÓN
# ---------------------------------

if __name__ == "__main__":

    root = tk.Tk()

    app = ControlActivosApp(root)

    root.mainloop()

# trabajo actual.
