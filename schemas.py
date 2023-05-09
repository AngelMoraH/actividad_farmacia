from pydantic import BaseModel
from typing import List


class Farmaceutico(BaseModel):
    id: int
    nombre: str
    genero: str
    class Config:
        orm_mode = True


class FarmaceuticoCreate(BaseModel):
    nombre: str
    genero: str


class Producto(BaseModel):
    id: int
    nombre: str
    fecha_caducidad: str
    precio: float
    stock : int
    almacen_id: int
    pedido_id : int

    class Config:
        orm_mode = True



class ProductoCreate(BaseModel):
    nombre: str
    fecha_caducidad: str
    precio: float
    stock : int
    almacen_id: int
    pedido_id : int | None = None

class Pedido(BaseModel):
    id: int
    cliente_id: int
    farmaceutico_id: int
    productos: List[Producto] = []
    cantidad: int
    total: float
    fecha: str

    class Config:
        orm_mode = True


class PedidoCreate(BaseModel):
    cliente_id: int
    farmaceutico_id: int
    productos: List[Producto] = []
    cantidad: int
    total: float
    fecha: str

class Cliente(BaseModel):
    id: int
    nombre: str
    saldo: int
    pedido: List[Pedido] = []
    class Config:
        orm_mode = True

class ClienteCreate(BaseModel):
    nombre: str
    saldo: int


Cliente.update_forward_refs()

class Almacen(BaseModel):
    id: int
    productos: List[Producto] = []
    cantidad: int

    class Config:
        orm_mode = True


class AlmacenCreate(BaseModel):
    productos: List[Producto]  = []
    cantidad: int


