def construir_controlador_cliente(cliente_repositorio):
    def obtener_datos():
        clientes = cliente_repositorio.obtener_todos()
        return [(c.id, c.nombre, c.apellido, c.telefono) for c in clientes]

    def crear_registro(valores):
        cliente_repositorio.crear(
            nombre=valores["nombre"],
            apellido=valores["apellido"],
            telefono=valores["telefono"],
        )

    def actualizar_registro(id_cliente, valores):
        cliente_repositorio.actualizar(
            id_cliente=id_cliente,
            nombre=valores["nombre"],
            apellido=valores["apellido"],
            telefono=valores["telefono"],
        )

    def eliminar_registro(id_cliente):
        cliente_repositorio.eliminar(id_cliente)

    campos = [
        {"clave": "nombre", "etiqueta": "Nombre:", "tipo": "entry"},
        {"clave": "apellido", "etiqueta": "Apellido:", "tipo": "entry"},
        {"clave": "telefono", "etiqueta": "Telefono:", "tipo": "entry"},
    ]

    columnas = [
        ("id", "ID"),
        ("nombre", "Nombre"),
        ("apellido", "Apellido"),
        ("telefono", "Telefono"),
    ]

    return {
        "titulo": "Datos del Cliente",
        "campos": campos,
        "columnas": columnas,
        "obtener_datos": obtener_datos,
        "crear_registro": crear_registro,
        "actualizar_registro": actualizar_registro,
        "eliminar_registro": eliminar_registro,
        "validador_extra": None,
    }
