import math
import re
import tkinter as tk

from datos import BaseDatos
from interfaz import VentanaPrincipal


def validar_cliente(valores, datos, id_actual=None):
    dni = valores["dni"]
    if not re.fullmatch(r"[0-9]{7,8}", dni):
        return "El DNI debe tener 7 u 8 dígitos, sin puntos ni espacios."
    if datos.dni_en_uso(dni, id_actual):
        return "Ya existe un cliente con ese DNI."

    telefono = valores["telefono"]
    if not re.fullmatch(r"\+?[0-9() -]+", telefono) or not 7 <= sum(
        caracter.isdigit() for caracter in telefono
    ) <= 15:
        return "El teléfono debe tener entre 7 y 15 dígitos. Puede incluir +, espacios y guiones."

    if not re.fullmatch(r"[^\s@]+@[^\s@]+\.[^\s@]+", valores["email"]):
        return "Ingresá un email válido, por ejemplo nombre@dominio.com."
    return None


def validar_pedido(valores, id_actual=None):
    if not re.fullmatch(r"[0-9]+", valores["cantidad"]):
        return "La cantidad debe ser un número entero válido."
    try:
        cantidad = int(valores["cantidad"])
    except ValueError:
        return "La cantidad debe ser un número entero válido."
    if cantidad <= 0 or cantidad > 9223372036854775807:
        return "La cantidad debe ser un entero positivo válido."

    if not re.fullmatch(r"[0-9]+(?:[.,][0-9]+)?", valores["precio"]):
        return "El precio debe ser un número válido."
    try:
        precio = float(valores["precio"].replace(",", "."))
    except ValueError:
        return "El precio debe ser un número válido."
    if not math.isfinite(precio) or precio <= 0:
        return "El precio debe ser un número mayor a cero."

    valores["cantidad"] = cantidad
    valores["precio"] = precio
    return None


def iniciar_aplicacion():
    datos = BaseDatos()

    def opciones_clientes():
        return [(id_cliente, f"{nombre} {apellido} (ID {id_cliente})")
                for id_cliente, nombre, apellido, *_ in datos.listar_clientes()]

    clientes = {
        "titulo": "Datos del Cliente",
        "campos": [
            {"clave": "nombre", "etiqueta": "Nombre:"},
            {"clave": "apellido", "etiqueta": "Apellido:"},
            {"clave": "dni", "etiqueta": "DNI:"},
            {"clave": "telefono", "etiqueta": "Teléfono:"},
            {"clave": "email", "etiqueta": "Email:"},
            {"clave": "direccion", "etiqueta": "Dirección:"},
        ],
        "columnas": [("id", "ID"), ("nombre", "Nombre"),
                     ("apellido", "Apellido"), ("dni", "DNI"),
                     ("telefono", "Teléfono"), ("email", "Email"),
                     ("direccion", "Dirección")],
        "listar": datos.listar_clientes,
        "agregar": datos.crear_cliente,
        "modificar": datos.actualizar_cliente,
        "borrar": datos.eliminar_cliente,
        "validar": lambda valores, id_actual: validar_cliente(valores, datos, id_actual),
    }

    pedidos = {
        "titulo": "Datos del Pedido",
        "campos": [
            {"clave": "cliente_id", "etiqueta": "Cliente:", "opciones": opciones_clientes},
            {"clave": "modelo", "etiqueta": "Modelo:"},
            {"clave": "material", "etiqueta": "Material:"},
            {"clave": "cantidad", "etiqueta": "Cantidad:"},
            {"clave": "precio", "etiqueta": "Precio:"},
            {"clave": "estado", "etiqueta": "Estado:",
             "opciones": lambda: [(estado, estado) for estado in
                                  ("Recibido", "En preparación", "Terminado")]},
        ],
        "columnas": [("id", "ID"), ("cliente", "Cliente"), ("modelo", "Modelo"),
                     ("material", "Material"), ("cantidad", "Cantidad"),
                     ("precio", "Precio"), ("estado", "Estado")],
        "listar": datos.listar_pedidos,
        "agregar": datos.crear_pedido,
        "modificar": datos.actualizar_pedido,
        "borrar": datos.eliminar_pedido,
        "validar": validar_pedido,
    }

    raiz = tk.Tk()
    VentanaPrincipal(raiz, clientes, pedidos, datos.cerrar)
    raiz.mainloop()


if __name__ == "__main__":
    iniciar_aplicacion()
