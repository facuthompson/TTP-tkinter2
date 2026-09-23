from tkinter import ttk


COLORES = {
    "fondo": "#eef2f9",
    "panel": "#e4ecf7",
    "borde": "#c3d3ea",
    "titulo": "#1b3a5c",
    "azul": "#2f7bd6",
    "verde": "#3fa64a",
    "rojo": "#d9483d",
    "gris": "#6b7785",
    "blanco": "#ffffff",
}

FUENTE = "Segoe UI"


def configurar_tema(raiz):
    raiz.configure(bg=COLORES["fondo"])
    estilo = ttk.Style(raiz)
    estilo.theme_use("clam")

    estilo.configure("TFrame", background=COLORES["fondo"])
    estilo.configure("Panel.TFrame", background=COLORES["panel"])
    estilo.configure("Titulo.TLabel", background=COLORES["panel"],
                     foreground=COLORES["titulo"], font=(FUENTE, 14, "bold"))
    estilo.configure("Campo.TLabel", background=COLORES["panel"],
                     foreground=COLORES["titulo"], font=(FUENTE, 10, "bold"))
    estilo.configure("TEntry", padding=5, font=(FUENTE, 10))
    estilo.configure("TCombobox", padding=5, font=(FUENTE, 10))

    estilo.configure("TNotebook", background=COLORES["titulo"], borderwidth=0)
    estilo.configure("TNotebook.Tab", background=COLORES["titulo"],
                     foreground=COLORES["blanco"], padding=(24, 12),
                     font=(FUENTE, 11, "bold"), borderwidth=0,
                     expand=(0, 0, 0, 0))
    estilo.map("TNotebook.Tab",
               background=[("selected", COLORES["azul"]), ("active", COLORES["titulo"])],
               foreground=[("selected", COLORES["blanco"]), ("active", COLORES["blanco"])],
               padding=[("selected", (24, 12)), ("!selected", (24, 12))],
               expand=[("selected", (0, 0, 0, 0)), ("!selected", (0, 0, 0, 0))])

    estilo.configure("Treeview", rowheight=27, font=(FUENTE, 10),
                     background=COLORES["blanco"], fieldbackground=COLORES["blanco"])
    estilo.configure("Treeview.Heading", background=COLORES["panel"],
                     foreground=COLORES["titulo"], font=(FUENTE, 10, "bold"))
    estilo.map("Treeview", background=[("selected", COLORES["azul"])],
               foreground=[("selected", COLORES["blanco"])])

    for nombre, color in (("Agregar", "verde"), ("Modificar", "azul"),
                          ("Borrar", "rojo"), ("Limpiar", "gris")):
        estilo.configure(f"{nombre}.TButton", background=COLORES[color],
                         foreground=COLORES["blanco"], padding=(16, 7),
                         font=(FUENTE, 10, "bold"), borderwidth=0)
        estilo.map(f"{nombre}.TButton",
                   background=[("active", COLORES[color]), ("pressed", COLORES[color])],
                   foreground=[("active", COLORES["blanco"])])
