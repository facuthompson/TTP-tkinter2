def construir_controlador_pedido(pedido_repositorio, cliente_repositorio):
    def obtener_datos():
        pedidos = pedido_repositorio.obtener_todos()
        return [
            (p.id, p.cliente_nombre, p.modelo, p.material, p.cantidad, p.precio, p.estado)
            for p in pedidos
        ]

    def opciones_clientes():
        clientes = cliente_repositorio.obtener_todos()
        return [(c.id, f"{c.nombre} {c.apellido}") for c in clientes]

    def opciones_estado():
        estados = ["Recibido", "En preparación", "Terminado"]
        return [(estado, estado) for estado in estados]

    def validar(valores):
        if not cliente_repositorio.obtener_todos():
            return "No hay clientes registrados. Cargá un cliente antes de crear un pedido."
        try:
            cantidad = int(valores["cantidad"])
            if cantidad <= 0:
                return "La cantidad debe ser un número entero mayor a cero."
        except ValueError:
            return "La cantidad debe ser un número entero válido."
        try:
            precio = float(valores["precio"])
            if precio <= 0:
                return "El precio debe ser un número mayor a cero."
        except ValueError:
            return "El precio debe ser un número válido."
        return None

    def crear_registro(valores):
        pedido_repositorio.crear(
            cliente_id=int(valores["cliente_id"]),
            modelo=valores["modelo"],
            material=valores["material"],
            cantidad=int(valores["cantidad"]),
            precio=float(valores["precio"]),
            estado=valores["estado"],
        )

    def actualizar_registro(id_pedido, valores):
        pedido_repositorio.actualizar(
            id_pedido=id_pedido,
            cliente_id=int(valores["cliente_id"]),
            modelo=valores["modelo"],
            material=valores["material"],
            cantidad=int(valores["cantidad"]),
            precio=float(valores["precio"]),
            estado=valores["estado"],
        )

    def eliminar_registro(id_pedido):
        pedido_repositorio.eliminar(id_pedido)

    campos = [
        {"clave": "cliente_id", "etiqueta": "Cliente:", "tipo": "combobox", "opciones": opciones_clientes},
        {"clave": "modelo", "etiqueta": "Modelo:", "tipo": "entry"},
        {"clave": "material", "etiqueta": "Material:", "tipo": "entry"},
        {"clave": "cantidad", "etiqueta": "Cantidad:", "tipo": "entry"},
        {"clave": "precio", "etiqueta": "Precio:", "tipo": "entry"},
        {"clave": "estado", "etiqueta": "Estado:", "tipo": "combobox", "opciones": opciones_estado},
    ]

    columnas = [
        ("id", "ID"),
        ("cliente", "Cliente"),
        ("modelo", "Modelo"),
        ("material", "Material"),
        ("cantidad", "Cantidad"),
        ("precio", "Precio"),
        ("estado", "Estado"),
    ]

    return {
        "titulo": "Datos del Pedido",
        "campos": campos,
        "columnas": columnas,
        "obtener_datos": obtener_datos,
        "crear_registro": crear_registro,
        "actualizar_registro": actualizar_registro,
        "eliminar_registro": eliminar_registro,
        "validador_extra": validar,
    }
