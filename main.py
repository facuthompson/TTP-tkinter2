import tkinter as tk

from interfaz.ventana_principal import VentanaPrincipal


def iniciar_aplicacion():
    raiz = tk.Tk()
    VentanaPrincipal(raiz)
    raiz.mainloop()


if __name__ == "__main__":
    iniciar_aplicacion()
