import sqlite3
from pathlib import Path


class BaseDatos:
    def __init__(self, ruta=None):
        self.ruta = Path(ruta) if ruta else Path(__file__).with_name("impresion3d.db")
        self.conexion = sqlite3.connect(self.ruta)
        self.conexion.execute("PRAGMA foreign_keys = ON")
        self.crear_tablas()

    def crear_tablas(self):
        with self.conexion:
            self.conexion.execute("""
                CREATE TABLE IF NOT EXISTS clientes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nombre TEXT NOT NULL,
                    apellido TEXT NOT NULL,
                    dni TEXT NOT NULL,
                    telefono TEXT NOT NULL,
                    email TEXT NOT NULL,
                    direccion TEXT NOT NULL
                )
            """)
            columnas = {
                fila[1] for fila in self.conexion.execute("PRAGMA table_info(clientes)")
            }
            for columna in ("dni", "email", "direccion"):
                if columna not in columnas:
                    self.conexion.execute(
                        f"ALTER TABLE clientes ADD COLUMN {columna} TEXT NOT NULL DEFAULT ''"
                    )
            self.conexion.execute("""
                CREATE TABLE IF NOT EXISTS pedidos (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    cliente_id INTEGER NOT NULL,
                    modelo TEXT NOT NULL,
                    material TEXT NOT NULL,
                    cantidad INTEGER NOT NULL,
                    precio REAL NOT NULL,
                    estado TEXT NOT NULL,
                    FOREIGN KEY (cliente_id) REFERENCES clientes(id)
                )
            """)

    def listar_clientes(self):
        return self.conexion.execute(
            "SELECT id, nombre, apellido, dni, telefono, email, direccion "
            "FROM clientes ORDER BY id"
        ).fetchall()

    def dni_en_uso(self, dni, excluir_id=None):
        fila = self.conexion.execute(
            "SELECT 1 FROM clientes WHERE dni = ? AND id != ? LIMIT 1",
            (dni, excluir_id if excluir_id is not None else -1),
        ).fetchone()
        return fila is not None

    def crear_cliente(self, nombre, apellido, dni, telefono, email, direccion):
        if self.dni_en_uso(dni):
            raise ValueError("Ya existe un cliente con ese DNI.")
        with self.conexion:
            self.conexion.execute(
                "INSERT INTO clientes (nombre, apellido, dni, telefono, email, direccion) "
                "VALUES (?, ?, ?, ?, ?, ?)",
                (nombre, apellido, dni, telefono, email, direccion),
            )

    def actualizar_cliente(self, id_cliente, nombre, apellido, dni, telefono, email, direccion):
        if self.dni_en_uso(dni, id_cliente):
            raise ValueError("Ya existe un cliente con ese DNI.")
        with self.conexion:
            self.conexion.execute(
                "UPDATE clientes SET nombre = ?, apellido = ?, dni = ?, telefono = ?, "
                "email = ?, direccion = ? WHERE id = ?",
                (nombre, apellido, dni, telefono, email, direccion, id_cliente),
            )

    def eliminar_cliente(self, id_cliente):
        pedidos = self.conexion.execute(
            "SELECT COUNT(*) FROM pedidos WHERE cliente_id = ?", (id_cliente,)
        ).fetchone()[0]
        if pedidos:
            raise ValueError("Este cliente tiene pedidos. Eliminá sus pedidos primero.")
        with self.conexion:
            self.conexion.execute("DELETE FROM clientes WHERE id = ?", (id_cliente,))

    def listar_pedidos(self):
        return self.conexion.execute("""
            SELECT pedidos.id, clientes.nombre || ' ' || clientes.apellido ||
                   ' (ID ' || clientes.id || ')',
                   pedidos.modelo, pedidos.material, pedidos.cantidad,
                   pedidos.precio, pedidos.estado
            FROM pedidos
            JOIN clientes ON clientes.id = pedidos.cliente_id
            ORDER BY pedidos.id
        """).fetchall()

    def crear_pedido(self, cliente_id, modelo, material, cantidad, precio, estado):
        with self.conexion:
            self.conexion.execute("""
                INSERT INTO pedidos (cliente_id, modelo, material, cantidad, precio, estado)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (cliente_id, modelo, material, cantidad, precio, estado))

    def actualizar_pedido(self, id_pedido, cliente_id, modelo, material, cantidad, precio, estado):
        with self.conexion:
            self.conexion.execute("""
                UPDATE pedidos
                SET cliente_id = ?, modelo = ?, material = ?, cantidad = ?, precio = ?, estado = ?
                WHERE id = ?
            """, (cliente_id, modelo, material, cantidad, precio, estado, id_pedido))

    def eliminar_pedido(self, id_pedido):
        with self.conexion:
            self.conexion.execute("DELETE FROM pedidos WHERE id = ?", (id_pedido,))

    def cerrar(self):
        self.conexion.close()
