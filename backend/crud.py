from sqlalchemy.orm import Session
import models
import schemas


# clientes controllers 
def get_cliente(db: Session, id: int):
    return db.query(models.cliente).filter(models.cliente.id == id).first()


def get_cliente_by_name(db: Session, nombre: str):
    return db.query(models.cliente).filter(models.cliente.nombre == nombre).first()


def get_clientes(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.cliente).order_by(models.cliente.id.asc()).offset(skip).limit(limit).all()


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
    return db.query(models.Farmacuetico).order_by(models.Farmacuetico.id.asc()).offset(skip).limit(limit).all()

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
    almacenes = db.query(models.Almacen).order_by(models.Almacen.id.asc()).offset(skip).limit(limit).all()
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
    return db.query(models.Producto).order_by(models.Producto.id.asc()).offset(skip).limit(limit).all()

def get_productos_by_name(db: Session, nombre: str):
    return db.query(models.Producto).filter(models.Producto.nombre.contains(nombre) ).all()

def add_producto(db: Session, producto: schemas.ProductoCreate):
    db_producto = models.Producto(nombre=producto.nombre, fecha_caducidad=producto.fecha_caducidad, precio=producto.precio, stock=producto.stock, almacen_id=producto.almacen_id, pedido_id = producto.pedido_id)
    print(db_producto)
    db.add(db_producto)
    db.commit()
    db.refresh(db_producto)
    return db_producto


def add_productos(db: Session):
    db_almacen = models.Almacen(cantidad=0)
    res=[]
    productos = [
        ["Diutin Protein", "2023-11-11", 70, 30, 1,None],
        ["ASPIRINA 100 MG", "2023-11-11", 6.40, 20, 1,None],
        ["TUKOL-D","2023-11-11", 20.15, 10, 1,None],
        ["NIKZON","2023-11-11", 14.10, 50, 1,None],
        ["BISMUTOL","2023-11-11", 28.90, 50, 1,None],
        ["CIRUELAX","2023-11-11", 19.90, 20, 1,None],
        ["Panadol","2023-11-11", 10.20, 20, 1,None],
        ["Amoxicilina","2023-11-11", 19.90, 20, 1,None],
        ["CICATRICURE","2023-11-11", 63.59, 30, 1,None],
        ["SILKA MEDIC","2023-11-11", 24.34, 20, 1,None]
    ]
    db.add(db_almacen)
    db.commit()
    db.refresh(db_almacen)

    db_cliente = models.cliente(nombre="Juan Perez", saldo=1000)
    db.add(db_cliente)
    db.commit()
    db.refresh(db_cliente)

    for i in range(10):
        db_producto = models.Producto(nombre=productos[i][0], fecha_caducidad=productos[i][1], precio=productos[i][2], stock=productos[i][3], almacen_id=productos[i][4], pedido_id = None)
        db.add(db_producto)
        res.append(db_producto)
        db.commit()
        db.refresh(db_producto)
        
    return res

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
    pedidos = db.query(models.Pedido).order_by(models.Pedido.id.asc()).offset(skip).limit(limit).all()
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

