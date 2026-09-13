import tkinter as tk
from tkinter import ttk

from datos.base_datos import BaseDatos
from datos.cliente_repositorio import ClienteRepositorio
from datos.pedido_repositorio import PedidoRepositorio
from controladores.cliente_controlador import construir_controlador_cliente
from controladores.pedido_controlador import construir_controlador_pedido
from interfaz.crud_frame import CRUDFrame


class VentanaPrincipal:
    def __init__(self, raiz):
        self.raiz = raiz
        self.raiz.title("Sistema de Impresión 3D")
        self.raiz.geometry("1050x680")
        self.raiz.configure(bg="#eef2f9")

        self.base_datos = BaseDatos()
        self.cliente_repositorio = ClienteRepositorio(self.base_datos)
        self.pedido_repositorio = PedidoRepositorio(self.base_datos)

        self._configurar_estilos()

        self.notebook = ttk.Notebook(self.raiz)
        self.notebook.pack(fill="both", expand=True)

        config_cliente = construir_controlador_cliente(self.cliente_repositorio)
        config_pedido = construir_controlador_pedido(self.pedido_repositorio, self.cliente_repositorio)

        self.marco_clientes = CRUDFrame(self.notebook, **config_cliente)
        self.marco_pedidos = CRUDFrame(self.notebook, **config_pedido)

        self.notebook.add(self.marco_clientes, text="Clientes")
        self.notebook.add(self.marco_pedidos, text="Pedidos")

        self.notebook.bind("<<NotebookTabChanged>>", self._al_cambiar_pestana)

    def _al_cambiar_pestana(self, evento):
        pestana_actual = self.notebook.index(self.notebook.select())
        if pestana_actual == 1:
            self.marco_pedidos.refrescar_combos()

    def _configurar_estilos(self):
        estilo = ttk.Style()
        estilo.theme_use("clam")

        estilo.configure("Fondo.TFrame", background="#eef2f9")

        estilo.configure("TNotebook", background="#1b3a5c", borderwidth=0, tabmargins=0)
        estilo.configure(
            "TNotebook.Tab",
            background="#1b3a5c",
            foreground="white",
            padding=(24, 14),
            font=("Segoe UI", 11, "bold"),
            borderwidth=0,
            relief="flat",
            focuscolor="#1b3a5c",
        )
        estilo.map(
            "TNotebook.Tab",
            background=[("selected", "#2f7bd6"), ("active", "#1b3a5c"), ("!selected", "#1b3a5c")],
            foreground=[("selected", "white"), ("active", "white"), ("!selected", "white")],
            padding=[("selected", (24, 14)), ("!selected", (24, 14))],
            relief=[("selected", "flat"), ("active", "flat"), ("!selected", "flat")],
            expand=[("selected", (0, 0, 0, 0)), ("!selected", (0, 0, 0, 0))],
        )

        estilo.configure("Treeview.Heading", background="#dbe6f5", foreground="#1b3a5c",
                        font=("Segoe UI", 10, "bold"), relief="flat")
        estilo.configure("Treeview", rowheight=26, font=("Segoe UI", 10), fieldbackground="white")
        estilo.map("Treeview", background=[("selected", "#2f7bd6")], foreground=[("selected", "white")])
