from sqlalchemy import  Column, Integer, String, ForeignKey, DOUBLE_PRECISION
from sqlalchemy.orm import relationship
from database import Base

class cliente(Base):
    __tablename__ ="clientes"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nombre = Column(String(200), unique=True)
    saldo = Column(Integer, default=0, nullable=False) 
    pedido = relationship("Pedido",backref="clientes") 

class Farmacuetico(Base):
    __tablename__ ="farmaceuticos"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nombre = Column(String(200), unique=True)
    genero = Column(String(1), nullable=False) 
    pedido = relationship("Pedido", backref="farmaceuticos")

class Almacen(Base):
    __tablename__ = "almacenes"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    productos = relationship("Producto", backref="almacenes") 
    cantidad = Column(Integer, default=0, nullable=False)

class Producto(Base):
    __tablename__ = "productos"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nombre = Column(String(200), unique=False, nullable=False)
    fecha_caducidad = Column(String(200), nullable=False)
    precio = Column(DOUBLE_PRECISION, default=0, nullable=False)
    stock = Column(Integer, default=0, nullable=False)
    almacen_id = Column(Integer, ForeignKey("almacenes.id"))
    pedido_id = Column(Integer, ForeignKey("pedidos.id"))


class Pedido(Base):
    __tablename__ = "pedidos"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    cliente_id = Column(Integer, ForeignKey("clientes.id"))
    farmaceutico_id = Column(Integer, ForeignKey("farmaceuticos.id"))
    productos = relationship("Producto", backref="pedidos") 
    cantidad = Column(Integer, default=0, nullable=False)
    total = Column(DOUBLE_PRECISION, default=0, nullable=False)
    fecha = Column(String(200), nullable=False)