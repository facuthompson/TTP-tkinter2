import sqlite3


class BaseDatos:
    def __init__(self, ruta_archivo="impresion3d.db"):
        self.ruta_archivo = ruta_archivo
        self.conexion = sqlite3.connect(self.ruta_archivo)
        self.conexion.execute("PRAGMA foreign_keys = ON")
        self._crear_tablas()

    def _crear_tablas(self):
        cursor = self.conexion.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS clientes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                apellido TEXT NOT NULL,
                telefono TEXT NOT NULL
            )
            """
        )
        cursor.execute(
            """
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
            """
        )
        self.conexion.commit()

    def obtener_cursor(self):
        return self.conexion.cursor()

    def confirmar(self):
        self.conexion.commit()

    def cerrar(self):
        self.conexion.close()
