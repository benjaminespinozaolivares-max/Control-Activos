import tkinter as tk

from login import LoginApp
from assets_log import ControlActivosApp


def iniciar_aplicacion(root, rut_usuario):

    # Limpiar la ventana del login
    for widget in root.winfo_children():
        widget.destroy()

    app = ControlActivosApp(root, rut_usuario)

    # Maximizar CONTROL-ACTIVOS
    root.state("zoomed")


def main():

    root = tk.Tk()

    LoginApp(
        root,
        on_success=lambda rut: iniciar_aplicacion(root, rut)
    )

    root.mainloop()


if __name__ == "__main__":
    main()
