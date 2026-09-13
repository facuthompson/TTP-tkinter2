from modelos.pedido import Pedido


class PedidoRepositorio:
    def __init__(self, base_datos):
        self.base_datos = base_datos

    def crear(self, cliente_id, modelo, material, cantidad, precio, estado):
        cursor = self.base_datos.obtener_cursor()
        cursor.execute(
            """
            INSERT INTO pedidos (cliente_id, modelo, material, cantidad, precio, estado)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (cliente_id, modelo, material, cantidad, precio, estado),
        )
        self.base_datos.confirmar()

    def actualizar(self, id_pedido, cliente_id, modelo, material, cantidad, precio, estado):
        cursor = self.base_datos.obtener_cursor()
        cursor.execute(
            """
            UPDATE pedidos
            SET cliente_id = ?, modelo = ?, material = ?, cantidad = ?, precio = ?, estado = ?
            WHERE id = ?
            """,
            (cliente_id, modelo, material, cantidad, precio, estado, id_pedido),
        )
        self.base_datos.confirmar()

    def eliminar(self, id_pedido):
        cursor = self.base_datos.obtener_cursor()
        cursor.execute("DELETE FROM pedidos WHERE id = ?", (id_pedido,))
        self.base_datos.confirmar()

    def obtener_todos(self):
        cursor = self.base_datos.obtener_cursor()
        cursor.execute(
            """
            SELECT pedidos.id, pedidos.cliente_id,
                   clientes.nombre || ' ' || clientes.apellido,
                   pedidos.modelo, pedidos.material, pedidos.cantidad,
                   pedidos.precio, pedidos.estado
            FROM pedidos
            JOIN clientes ON clientes.id = pedidos.cliente_id
            ORDER BY pedidos.id
            """
        )
        filas = cursor.fetchall()
        return [Pedido(*fila) for fila in filas]
