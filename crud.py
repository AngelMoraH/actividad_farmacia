from sqlalchemy.orm import Session
import models
import schemas


# clientes controllers 
def get_cliente(db: Session, id: int):
    return db.query(models.cliente).filter(models.cliente.id == id).first()


def get_cliente_by_name(db: Session, nombre: str):
    return db.query(models.cliente).filter(models.cliente.nombre == nombre).first()


def get_clientes(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.cliente).offset(skip).limit(limit).all()


def add_cliente(db: Session, cliente: schemas.ClienteCreate):
    db_cliente = models.cliente(nombre=cliente.nombre, saldo=cliente.saldo)
    db.add(db_cliente)
    db.commit()
    db.refresh(db_cliente)
    return db_cliente


# farmaceuticos controllers
def get_farmaceutico(db: Session, id: int):
    return db.query(models.Farmacuetico).filter(models.Farmacuetico.id == id).first()

def get_farmaceutico_by_name(db: Session, nombre: str):
    return db.query(models.Farmacuetico).filter(models.Farmacuetico.nombre == nombre).first()

def get_farmaceuticos(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Farmacuetico).offset(skip).limit(limit).all()

def add_farmaceutico(db: Session, farmaceutico: schemas.FarmaceuticoCreate):
    db_farmaceutico = models.Farmacuetico(nombre=farmaceutico.nombre, genero=farmaceutico.genero)
    db.add(db_farmaceutico)
    db.commit()
    db.refresh(db_farmaceutico)
    return db_farmaceutico


# almacenes controllers
def get_almacen(db: Session, id: int):
    almacen = db.query(models.Almacen).filter(models.Almacen.id == id).first()
    almacen.productos = db.query(models.Producto).filter(models.Producto.almacen_id == id).all()
    almacen.cantidad = len(almacen.productos)
    db.commit()
    db.refresh(almacen)
    return almacen

def get_almacenes(db: Session, skip: int = 0, limit: int = 100):
    almacenes = db.query(models.Almacen).offset(skip).limit(limit).all()
    for almacen in almacenes:
        almacen.productos = db.query(models.Producto).filter(models.Producto.almacen_id == almacen.id).all()
        almacen.cantidad = len(almacen.productos)
        db.commit()
        db.refresh(almacen)
    return almacenes

def add_almacen(db: Session, almacen: schemas.AlmacenCreate):
    db_almacen = models.Almacen(cantidad=almacen.cantidad)
    db.add(db_almacen)
    db.commit()
    db.refresh(db_almacen)
    return db_almacen


# productos controllers
def get_producto(db: Session, id: int):
    return db.query(models.Producto).filter(models.Producto.id == id).first()

def get_productos(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Producto).offset(skip).limit(limit).all()

def add_producto(db: Session, producto: schemas.ProductoCreate):
    db_producto = models.Producto(nombre=producto.nombre, fecha_caducidad=producto.fecha_caducidad, precio=producto.precio, stock=producto.stock, almacen_id=producto.almacen_id, pedido_id = producto.pedido_id)
    db.add(db_producto)
    db.commit()
    db.refresh(db_producto)
    return db_producto

# pedidos controllers
def get_pedido(db: Session, id: int):
    pedido = db.query(models.Pedido).filter(models.Pedido.id == id).first()
    if pedido is None:
        return None
    else:
        pedido.productos = db.query(models.Producto).filter(models.Producto.pedido_id == id).all()
        pedido.cantidad = len(pedido.productos)
        pedido.total = 0
        for producto in pedido.productos:
            pedido.total += producto.precio
        db.commit()
        db.refresh(pedido)
        
        return pedido

def get_pedidos(db: Session, skip: int = 0, limit: int = 100):
    pedidos = db.query(models.Pedido).offset(skip).limit(limit).all()
    for pedido in pedidos:
        pedido.productos = db.query(models.Producto).filter(models.Producto.pedido_id == pedido.id).all()
        pedido.cantidad = len(pedido.productos)
        pedido.total = 0
        for producto in pedido.productos:
            pedido.total += producto.precio
        db.commit()
        db.refresh(pedido)
    return pedidos

def add_pedido(db: Session, pedido: schemas.PedidoCreate):
    db_pedido = models.Pedido(cliente_id=pedido.cliente_id, farmaceutico_id=pedido.farmaceutico_id, cantidad=pedido.cantidad, total=pedido.total, fecha=pedido.fecha)
    db.add(db_pedido)
    db.commit()
    db.refresh(db_pedido)
    return db_pedido

