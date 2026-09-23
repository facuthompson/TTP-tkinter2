import tkinter as tk
from tkinter import messagebox, ttk

from tema import configurar_tema


class CRUDFrame(ttk.Frame):
    def __init__(self, contenedor, config):
        super().__init__(contenedor)
        self.configuracion = config
        self.campos = {}
        self.opciones = {}
        self.id_seleccionado = None

        self.crear_formulario()
        self.crear_botones()
        self.crear_tabla()
        self.actualizar()

    def crear_formulario(self):
        panel = ttk.Frame(self, style="Panel.TFrame", padding=20)
        panel.pack(fill="x", padx=16, pady=(16, 8))
        ttk.Label(panel, text=self.configuracion["titulo"], style="Titulo.TLabel").pack(anchor="w")
        ttk.Separator(panel).pack(fill="x", pady=12)

        formulario = ttk.Frame(panel, style="Panel.TFrame")
        formulario.pack(fill="x")
        formulario.columnconfigure(1, weight=1)
        formulario.columnconfigure(3, weight=1)

        for indice, campo in enumerate(self.configuracion["campos"]):
            fila, lado = indice % 3, (indice // 3) * 2
            ttk.Label(formulario, text=campo["etiqueta"], style="Campo.TLabel").grid(
                row=fila, column=lado, sticky="w", padx=(0, 10), pady=7
            )
            if "opciones" in campo:
                widget = ttk.Combobox(formulario, state="readonly")
            else:
                widget = ttk.Entry(formulario)
            widget.grid(row=fila, column=lado + 1, sticky="ew", padx=(0, 25), pady=7)
            self.campos[campo["clave"]] = widget

    def crear_botones(self):
        panel = ttk.Frame(self)
        panel.pack(pady=10)
        acciones = (("Agregar", self.agregar), ("Modificar", self.modificar),
                    ("Borrar", self.borrar), ("Limpiar", self.limpiar))
        for texto, accion in acciones:
            ttk.Button(panel, text=texto, command=accion, style=f"{texto}.TButton").pack(
                side="left", padx=5
            )

    def crear_tabla(self):
        panel = ttk.Frame(self)
        panel.pack(fill="both", expand=True, padx=16, pady=(0, 16))
        columnas = self.configuracion["columnas"]
        self.tabla = ttk.Treeview(panel, columns=[clave for clave, _ in columnas],
                                  show="headings", height=12)
        for clave, titulo in columnas:
            self.tabla.heading(clave, text=titulo)
            self.tabla.column(clave, anchor="center", width=130)
        barra = ttk.Scrollbar(panel, orient="vertical", command=self.tabla.yview)
        self.tabla.configure(yscrollcommand=barra.set)
        self.tabla.pack(side="left", fill="both", expand=True)
        barra.pack(side="right", fill="y")
        self.tabla.bind("<<TreeviewSelect>>", self.seleccionar)

    def actualizar(self):
        for campo in self.configuracion["campos"]:
            if "opciones" in campo:
                opciones = campo["opciones"]()
                mapa = {texto: valor for valor, texto in opciones}
                self.opciones[campo["clave"]] = mapa
                self.campos[campo["clave"]]["values"] = list(mapa)
        for fila in self.tabla.get_children():
            self.tabla.delete(fila)
        for registro in self.configuracion["listar"]():
            self.tabla.insert("", "end", values=registro)
        self.limpiar()

    def seleccionar(self, evento=None):
        seleccion = self.tabla.selection()
        if not seleccion:
            return
        valores = self.tabla.item(seleccion[0], "values")
        self.id_seleccionado = int(valores[0])
        for indice, campo in enumerate(self.configuracion["campos"], start=1):
            widget = self.campos[campo["clave"]]
            if "opciones" in campo:
                widget.set(valores[indice])
            else:
                widget.delete(0, tk.END)
                widget.insert(0, valores[indice])

    def leer_formulario(self):
        valores = {}
        for campo in self.configuracion["campos"]:
            clave = campo["clave"]
            texto = self.campos[clave].get().strip()
            valores[clave] = self.opciones[clave].get(texto) if "opciones" in campo else texto
        return valores

    def validar(self, valores, modificar=False):
        if any(valor is None or valor == "" for valor in valores.values()):
            return "Todos los campos son obligatorios."
        validador = self.configuracion.get("validar")
        id_actual = self.id_seleccionado if modificar else None
        return validador(valores, id_actual) if validador else None

    def guardar(self, modificar=False):
        if modificar and self.id_seleccionado is None:
            messagebox.showwarning("Sin selección", "Seleccioná un registro de la tabla primero.")
            return
        valores = self.leer_formulario()
        error = self.validar(valores, modificar)
        if error:
            messagebox.showwarning("Datos inválidos", error)
            return
        try:
            if modificar:
                self.configuracion["modificar"](self.id_seleccionado, **valores)
            else:
                self.configuracion["agregar"](**valores)
        except ValueError as error:
            messagebox.showerror("No se pudo guardar", str(error))
            return
        self.actualizar()

    def agregar(self):
        self.guardar()

    def modificar(self):
        self.guardar(modificar=True)

    def borrar(self):
        if self.id_seleccionado is None:
            messagebox.showwarning("Sin selección", "Seleccioná un registro de la tabla primero.")
            return
        if not messagebox.askyesno("Confirmar borrado", "¿Seguro que querés eliminar este registro?"):
            return
        try:
            self.configuracion["borrar"](self.id_seleccionado)
        except ValueError as error:
            messagebox.showwarning("No se pudo borrar", str(error))
            return
        self.actualizar()

    def limpiar(self):
        for widget in self.campos.values():
            if isinstance(widget, ttk.Combobox):
                widget.set("")
            else:
                widget.delete(0, tk.END)
        if self.tabla.selection():
            self.tabla.selection_remove(self.tabla.selection())
        self.id_seleccionado = None


class VentanaPrincipal:
    def __init__(self, raiz, config_clientes, config_pedidos, cerrar):
        raiz.title("Sistema de Impresión 3D")
        raiz.geometry("1050x680")
        configurar_tema(raiz)

        pestanas = ttk.Notebook(raiz)
        pestanas.pack(fill="both", expand=True)
        self.clientes = CRUDFrame(pestanas, config_clientes)
        self.pedidos = CRUDFrame(pestanas, config_pedidos)
        pestanas.add(self.clientes, text="Clientes")
        pestanas.add(self.pedidos, text="Pedidos")
        pestanas.bind("<<NotebookTabChanged>>", lambda evento: self.pedidos.actualizar()
                      if pestanas.select() == str(self.pedidos) else None)

        def salir():
            cerrar()
            raiz.destroy()

        raiz.protocol("WM_DELETE_WINDOW", salir)
