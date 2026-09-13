from modelos.cliente import Cliente


class ClienteRepositorio:
    def __init__(self, base_datos):
        self.base_datos = base_datos

    def crear(self, nombre, apellido, telefono):
        cursor = self.base_datos.obtener_cursor()
        cursor.execute(
            "INSERT INTO clientes (nombre, apellido, telefono) VALUES (?, ?, ?)",
            (nombre, apellido, telefono),
        )
        self.base_datos.confirmar()

    def actualizar(self, id_cliente, nombre, apellido, telefono):
        cursor = self.base_datos.obtener_cursor()
        cursor.execute(
            "UPDATE clientes SET nombre = ?, apellido = ?, telefono = ? WHERE id = ?",
            (nombre, apellido, telefono, id_cliente),
        )
        self.base_datos.confirmar()

    def eliminar(self, id_cliente):
        cursor = self.base_datos.obtener_cursor()
        cursor.execute("DELETE FROM clientes WHERE id = ?", (id_cliente,))
        self.base_datos.confirmar()

    def obtener_todos(self):
        cursor = self.base_datos.obtener_cursor()
        cursor.execute("SELECT id, nombre, apellido, telefono FROM clientes ORDER BY id")
        filas = cursor.fetchall()
        return [Cliente(*fila) for fila in filas]
