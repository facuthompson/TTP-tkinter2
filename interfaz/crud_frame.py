import tkinter as tk
from tkinter import ttk, messagebox


class CRUDFrame(ttk.Frame):

    def __init__(
    self,
        contenedor,
        titulo,
        campos,
        columnas,
        obtener_datos,
        crear_registro,
        actualizar_registro,
        eliminar_registro,
        validador_extra=None
    ):
        super().__init__(contenedor)

        self.titulo = titulo
        self.campos = campos
        self.columnas = columnas
        self.obtener_datos = obtener_datos
        self.crear_registro = crear_registro
        self.actualizar_registro = actualizar_registro
        self.eliminar_registro = eliminar_registro
        self.validador_extra = validador_extra

        self.widgets = {}
        self.opciones_mapa = {}
        self.id_seleccionado = None

        self.configure(style="Fondo.TFrame")

        self._construir_panel_formulario()
        self._construir_panel_botones()
        self._construir_tabla()

        self.refrescar_combos()
        self.refrescar_tabla()

    def _construir_panel_formulario(self):
        panel = tk.Frame(
            self,
            bg="#e4ecf7",
            highlightbackground="#c3d3ea",
            highlightthickness=1
        )
        panel.pack(fill="x", padx=15, pady=(15, 5))

        encabezado = tk.Frame(panel, bg="#e4ecf7")
        encabezado.pack(fill="x", padx=20, pady=(15, 10))

        circulo = tk.Canvas(
            encabezado,
            width=32,
            height=32,
            bg="#e4ecf7",
            highlightthickness=0
        )
        circulo.create_oval(
            2, 2, 30, 30,
            fill="#2f7bd6",
            outline=""
        )
        circulo.pack(side="left", padx=(0, 12))

        tk.Label(
            encabezado,
            text=self.titulo,
            bg="#e4ecf7",
            fg="#1b3a5c",
            font=("Segoe UI", 14, "bold")
        ).pack(side="left")

        ttk.Separator(
            panel,
            orient="horizontal"
        ).pack(fill="x")

        formulario = tk.Frame(
            panel,
            bg="#e4ecf7"
        )
        formulario.pack(
            fill="x",
            padx=25,
            pady=18
        )

        formulario.grid_columnconfigure(1, weight=1)
        formulario.grid_columnconfigure(3, weight=1)

        for indice, campo in enumerate(self.campos):

            if indice < 3:
                fila = indice
                columna = 0
            else:
                fila = indice - 3
                columna = 2

            tk.Label(
                formulario,
                text=campo["etiqueta"],
                bg="#e4ecf7",
                fg="#1b3a5c",
                font=("Segoe UI", 10, "bold")
            ).grid(
                row=fila,
                column=columna,
                sticky="w",
                padx=(0, 10),
                pady=7
            )

            if campo["tipo"] == "combobox":
                widget = ttk.Combobox(
                    formulario,
                    state="readonly",
                    width=30,
                    font=("Segoe UI", 10)
                )
            else:
                widget = tk.Entry(
                    formulario,
                    width=32,
                    font=("Segoe UI", 10),
                    relief="solid",
                    bd=1,
                    highlightthickness=0
                )

            widget.grid(
                row=fila,
                column=columna + 1,
                sticky="ew",
                padx=(0, 35),
                pady=7
            )

            self.widgets[campo["clave"]] = widget

    def _construir_panel_botones(self):
        panel = tk.Frame(
            self,
            bg="#eef2f9"
        )
        panel.pack(
            fill="x",
            padx=15,
            pady=(5, 15)
        )

        botones = tk.Frame(
            panel,
            bg="#eef2f9"
        )
        botones.pack(anchor="center")

        tk.Button(
            botones,
            text="Agregar",
            bg="#3fa64a",
            fg="white",
            activebackground="#369941",
            activeforeground="white",
            font=("Segoe UI", 10, "bold"),
            relief="flat",
            width=14,
            height=1,
            cursor="hand2",
            command=self._agregar
        ).pack(side="left", padx=5)

        tk.Button(
            botones,
            text="Modificar",
            bg="#2f7bd6",
            fg="white",
            activebackground="#2a6cbe",
            activeforeground="white",
            font=("Segoe UI", 10, "bold"),
            relief="flat",
            width=14,
            height=1,
            cursor="hand2",
            command=self._modificar
        ).pack(side="left", padx=5)

        tk.Button(
            botones,
            text="Borrar",
            bg="#d9483d",
            fg="white",
            activebackground="#c33f35",
            activeforeground="white",
            font=("Segoe UI", 10, "bold"),
            relief="flat",
            width=14,
            height=1,
            cursor="hand2",
            command=self._borrar
        ).pack(side="left", padx=5)

        tk.Button(
            botones,
            text="Limpiar",
            bg="#6b7785",
            fg="white",
            activebackground="#5d6875",
            activeforeground="white",
            font=("Segoe UI", 10, "bold"),
            relief="flat",
            width=14,
            height=1,
            cursor="hand2",
            command=self.limpiar
        ).pack(side="left", padx=5)

    def _construir_tabla(self):
        panel = tk.Frame(
            self,
            bg="#eef2f9"
        )
        panel.pack(
            fill="both",
            expand=True,
            padx=15,
            pady=(0, 15)
        )

        claves = [clave for clave, _ in self.columnas]

        self.tabla = ttk.Treeview(
            panel,
            columns=claves,
            show="headings",
            height=12
        )
        

        for clave, encabezado in self.columnas:
            self.tabla.heading(
                clave,
                text=encabezado
            )
            self.tabla.column(
                clave,
                anchor="center"
            )

        barra = ttk.Scrollbar(
            panel,
            orient="vertical",
            command=self.tabla.yview
        )

        self.tabla.configure(
            yscrollcommand=barra.set
        )

        self.tabla.pack(
            side="left",
            fill="both",
            expand=True
        )

        barra.pack(
            side="right",
            fill="y"
        )

        self.tabla.bind(
    "<<TreeviewSelect>>",
    self._seleccionar_fila
        )

    def refrescar_combos(self):
        for campo in self.campos:

            if campo["tipo"] != "combobox":
                continue

            opciones = (
                campo["opciones"]()
                if callable(campo["opciones"])
                else campo["opciones"]
            )

            mapa = {
                texto: valor
                for valor, texto in opciones
            }

            self.opciones_mapa[campo["clave"]] = mapa

            self.widgets[
                campo["clave"]
            ]["values"] = list(mapa.keys())

    def refrescar_tabla(self):
        for fila in self.tabla.get_children():
            self.tabla.delete(fila)

        for registro in self.obtener_datos():
            self.tabla.insert(
                "",
                "end",
                values=registro
            )

    def _seleccionar_fila(self, evento):
        seleccion = self.tabla.selection()

        if not seleccion:
            return

        valores = self.tabla.item(
            seleccion[0],
            "values"
        )

        self.id_seleccionado = valores[0]

        for indice, campo in enumerate(
            self.campos,
            start=1
        ):
            valor_columna = (
                valores[indice]
                if indice < len(valores)
                else ""
            )

            widget = self.widgets[
                campo["clave"]
            ]

            if campo["tipo"] == "combobox":
                widget.set(str(valor_columna))
            else:
                widget.delete(0, tk.END)
                widget.insert(0, valor_columna)

    def leer_valores(self):
        valores = {}

        for campo in self.campos:
            widget = self.widgets[
                campo["clave"]
            ]

            if campo["tipo"] == "combobox":
                texto = widget.get()

                mapa = self.opciones_mapa.get(
                    campo["clave"],
                    {}
                )

                valores[
                    campo["clave"]
                ] = mapa.get(texto)
            else:
                valores[
                    campo["clave"]
                ] = widget.get().strip()

        return valores

    def _hay_campos_vacios(self, valores):
        for campo in self.campos:
            valor = valores[
                campo["clave"]
            ]

            if valor is None or valor == "":
                return True

        return False

    def _agregar(self):
        valores = self.leer_valores()

        if self._hay_campos_vacios(valores):
            messagebox.showwarning(
                "Campos incompletos",
                "Todos los campos son obligatorios."
            )
            return

        if self.validador_extra:
            error = self.validador_extra(valores)

            if error:
                messagebox.showwarning(
                    "Datos inválidos",
                    error
                )
                return

        self.crear_registro(valores)
        self.refrescar_tabla()
        self.limpiar()

    def _modificar(self):
        if not self.id_seleccionado:
            messagebox.showwarning(
                "Sin selección",
                "Seleccioná un registro de la tabla primero."
            )
            return

        valores = self.leer_valores()

        if self._hay_campos_vacios(valores):
            messagebox.showwarning(
                "Campos incompletos",
                "Todos los campos son obligatorios."
            )
            return

        if self.validador_extra:
            error = self.validador_extra(valores)

            if error:
                messagebox.showwarning(
                    "Datos inválidos",
                    error
                )
                return

        self.actualizar_registro(
            self.id_seleccionado,
            valores
        )

        self.refrescar_tabla()
        self.limpiar()

    def _borrar(self):
        if not self.id_seleccionado:
            messagebox.showwarning(
                "Sin selección",
                "Seleccioná un registro de la tabla primero."
            )
            return

        confirmar = messagebox.askyesno(
            "Confirmar borrado",
            "¿Seguro que querés eliminar este registro?"
        )

        if not confirmar:
            return

        self.eliminar_registro(
            self.id_seleccionado
        )

        self.refrescar_tabla()
        self.limpiar()

    def limpiar(self):
        for campo in self.campos:
            widget = self.widgets[
                campo["clave"]
            ]

            if campo["tipo"] == "combobox":
                widget.set("")
            else:
                widget.delete(0, tk.END)

        seleccion_actual = self.tabla.selection()

        if seleccion_actual:
            self.tabla.selection_remove(
                seleccion_actual
            )

        self.id_seleccionado = None
