from dataclasses import dataclass


@dataclass
class Pedido:
    id: int
    cliente_id: int
    cliente_nombre: str
    modelo: str
    material: str
    cantidad: int
    precio: float
    estado: str
