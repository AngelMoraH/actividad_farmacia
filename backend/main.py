from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import crud
import models
import schemas
from database import SessionLocal, engine


models.Base.metadata.create_all(bind=engine)

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/",response_model=list[schemas.Producto])
def add_productos_all(db: Session = Depends(get_db)):
    return crud.add_productos(db)

# clientes endpoints
@app.post("/clientes", response_model=schemas.Cliente)
def create_cliente(clienteschema: schemas.ClienteCreate, db: Session = Depends(get_db)):
    db_cliente = crud.get_cliente_by_name(db, nombre=clienteschema.nombre)
    if db_cliente:
        raise HTTPException(status_code=400, detail="cliente already registered")
    return crud.add_cliente(db=db, cliente=clienteschema)


@app.get("/clientes", response_model=list[schemas.Cliente])
def read_clientes(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    clientes = crud.get_clientes(db, skip=skip, limit=limit)
    return clientes


@app.get("/clientes/{cliente_id}", response_model=schemas.Cliente)
def read_cliente(cliente_id: int, db: Session = Depends(get_db)):
    db_cliente = crud.get_cliente(db, id=cliente_id)
    if db_cliente is None:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    return db_cliente

@app.put("/clientes/{cliente_id}", response_model=schemas.Cliente)
def update_cliente(cliente_id: int, cliente: schemas.ClienteCreate, db: Session = Depends(get_db)):
    db_cliente = crud.get_cliente(db, id=cliente_id)
    if db_cliente is None:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    db_cliente.nombre = cliente.nombre
    db_cliente.saldo = cliente.saldo
    db.commit()
    db.refresh(db_cliente)
    return db_cliente


@app.put("/clientes/{cliente_id}/remove_saldo/{saldo}", response_model=schemas.Cliente)
def remove_saldo(cliente_id: int, saldo: float, db: Session = Depends(get_db)):
    db_cliente = crud.get_cliente(db, id=cliente_id)
    if db_cliente is None:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    if db_cliente.saldo < saldo:
        raise HTTPException(status_code=404, detail="Saldo insuficiente")
    db_cliente.saldo = db_cliente.saldo - saldo
    db.commit()
    db.refresh(db_cliente)
    return db_cliente

@app.delete("/clientes/{cliente_id}", response_model=schemas.Cliente)
def delete_user(cliente_id: int, db: Session = Depends(get_db)):

    db_cliente = crud.get_cliente(db, id=cliente_id)
    for pedido in db_cliente.pedido:
        db.delete(pedido)
    if db_cliente is None:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    db.delete(db_cliente)
    db.commit()
    return db_cliente


# farmaceuticos endpoints
@app.post("/farmaceuticos", response_model=schemas.Farmaceutico)  
def create_farmaceutico(farmaceuticoschema: schemas.FarmaceuticoCreate, db: Session = Depends(get_db)):
    db_farmaceutico = crud.get_farmaceutico_by_name(db, nombre=farmaceuticoschema.nombre)
    if db_farmaceutico:
        raise HTTPException(status_code=400, detail="Farmaceutico already registered")
    return crud.add_farmaceutico(db=db, farmaceutico=farmaceuticoschema)

@app.get("/farmaceuticos", response_model=list[schemas.Farmaceutico])
def read_farmaceuticos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    farmaceuticos = crud.get_farmaceuticos(db, skip=skip, limit=limit)
    return farmaceuticos

@app.get("/farmaceuticos/{farmaceutico_id}", response_model=schemas.Farmaceutico)
def read_farmaceutico(farmaceutico_id: int, db: Session = Depends(get_db)):
    db_farmaceutico = crud.get_farmaceutico(db, id=farmaceutico_id)
    if db_farmaceutico is None:
        raise HTTPException(status_code=404, detail="Farmaceutico no encontrado")
    return db_farmaceutico

@app.put("/farmaceuticos/{farmaceutico_id}", response_model=schemas.Farmaceutico)
def update_farmaceutico(farmaceutico_id: int, farmaceutico: schemas.FarmaceuticoCreate, db: Session = Depends(get_db)):
    db_farmaceutico = crud.get_farmaceutico(db, id=farmaceutico_id)
    if db_farmaceutico is None:
        raise HTTPException(status_code=404, detail="Farmaceutico no encontrado")
    db_farmaceutico.nombre = farmaceutico.nombre
    db_farmaceutico.genero = farmaceutico.genero
    db.commit()
    db.refresh(db_farmaceutico)
    return db_farmaceutico

@app.delete("/farmaceuticos/{farmaceutico_id}", response_model=schemas.Farmaceutico)
def delete_farmaceutico(farmaceutico_id: int, db: Session = Depends(get_db)):
    db_farmaceutico = crud.get_farmaceutico(db, id=farmaceutico_id)
    if db_farmaceutico is None:
        raise HTTPException(status_code=404, detail="Farmaceutico no encontrado")
    db.delete(db_farmaceutico)
    db.commit()
    return db_farmaceutico


# almacenes endpoints
@app.post("/almacenes", response_model=schemas.Almacen)
def create_almacen(almacenschema: schemas.AlmacenCreate, db: Session = Depends(get_db)):
    return crud.add_almacen(db=db, almacen=almacenschema)

@app.get("/almacenes", response_model=list[schemas.Almacen])
def read_almacenes(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    almacenes = crud.get_almacenes(db, skip=skip, limit=limit)
    return almacenes

@app.get("/almacenes/{almacen_id}", response_model=schemas.Almacen)
def read_almacen(almacen_id: int, db: Session = Depends(get_db)):
    db_almacen = crud.get_almacen(db, id=almacen_id)
    if db_almacen is None:
        raise HTTPException(status_code=404, detail="Almacen no encontrado")
    return db_almacen


@app.put("/almacenes/{almacen_id}", response_model=schemas.Almacen)
def update_almacen(almacen_id: int, almacen: schemas.AlmacenCreate, db: Session = Depends(get_db)):
    db_almacen = crud.get_almacen(db, id=almacen_id)
    if db_almacen is None:
        raise HTTPException(status_code=404, detail="Almacen no encontrado")
    db_almacen.nombre = almacen.nombre
    db_almacen.cantidad = almacen.cantidad
    db.commit()
    db.refresh(db_almacen)
    return db_almacen

@app.put("/almacenes/{almacen_id}/remove_producto/{producto_id}", response_model=schemas.Almacen)
def remove_producto_almacen(almacen_id: int, producto_id: int, db: Session = Depends(get_db)):
    db_almacen = crud.get_almacen(db, id=almacen_id)
    if db_almacen is None:
        raise HTTPException(status_code=404, detail="Pedido no encontrado")
    db_producto = crud.get_producto(db, id=producto_id)
    if db_producto is None:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    db_producto.pedido_id = None
    db_almacen.productos.remove(db_producto)
    db.commit()
    db.refresh(db_almacen)
    db.refresh(db_producto)
    return db_almacen

@app.delete("/almacenes/{almacen_id}", response_model=schemas.Almacen)
def delete_almacen(almacen_id: int, db: Session = Depends(get_db)):
    db_almacen = crud.get_almacen(db, id=almacen_id)
    if db_almacen is None:
        raise HTTPException(status_code=404, detail="Almacen no encontrado")
    db.delete(db_almacen)
    db.commit()
    return db_almacen



# productos endpoints
@app.post("/productos", response_model=schemas.Producto)
def create_producto(productoschema: schemas.ProductoCreate, db: Session = Depends(get_db)):
    print("entra al endpoint")
    return crud.add_producto(db=db, producto=productoschema)

@app.get("/productos", response_model=list[schemas.Producto])
def read_productos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    productos = crud.get_productos(db, skip=skip, limit=limit)
    return productos

@app.get("/productos/{producto_name}", response_model=list[schemas.Producto])
def read_productos_by_name(producto_name: str, db: Session = Depends(get_db)):
    productos = crud.get_productos_by_name(db, nombre=producto_name)
    return productos

@app.get("/productos/{producto_id}", response_model=schemas.Producto)
def read_producto(producto_id: int, db: Session = Depends(get_db)):
    db_producto = crud.get_producto(db, id=producto_id)
    if db_producto is None:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return db_producto

@app.get("/productos/add_stock/{producto_id}", response_model=schemas.Producto)
def add_stock(producto_id: int, db: Session = Depends(get_db)):
    db_producto = crud.get_producto(db, id=producto_id)
    if db_producto is None:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    db_producto.stock = db_producto.stock + 1
    db.commit()
    db.refresh(db_producto)
    return db_producto

@app.get("/productos/remove_stock/{producto_id}", response_model=schemas.Producto)
def remove_stock(producto_id: int, db: Session = Depends(get_db)):
    db_producto = crud.get_producto(db, id=producto_id)
    if db_producto is None:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    if db_producto.stock == 0:
        raise HTTPException(status_code=404, detail="Producto agotado")
    db_producto.stock = db_producto.stock - 1
    db.commit()
    db.refresh(db_producto)
    return db_producto


@app.put("/productos/{producto_id}", response_model=schemas.Producto)
def update_producto(producto_id: int, producto: schemas.ProductoCreate, db: Session = Depends(get_db)):
    db_producto = crud.get_producto(db, id=producto_id)
    if db_producto is None:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    db_producto.nombre = producto.nombre
    db_producto.fecha_caducidad = producto.fecha_caducidad
    db_producto.precio = producto.precio
    db_producto.stock = producto.stock
    db_producto.almacen_id = producto.almacen_id
    db_producto.pedido_id = producto.pedido_id
    db.commit()
    db.refresh(db_producto)
    return db_producto

@app.delete("/productos/{producto_id}", response_model=schemas.Producto)
def delete_producto(producto_id: int, db: Session = Depends(get_db)):
    db_producto = crud.get_producto(db, id=producto_id)
    if db_producto is None:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    db.delete(db_producto)
    db.commit()
    return db_producto


# pedidos endpoints
@app.post("/pedidos", response_model=schemas.Pedido)
def create_pedido(pedidoschema: schemas.PedidoCreate, db: Session = Depends(get_db)):
    return crud.add_pedido(db=db, pedido=pedidoschema)

@app.get("/pedidos", response_model=list[schemas.Pedido])
def read_pedidos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    pedidos = crud.get_pedidos(db, skip=skip, limit=limit)
    return pedidos

@app.get("/pedidos/{pedido_id}", response_model=schemas.Pedido)
def read_pedido(pedido_id: int, db: Session = Depends(get_db)):
    db_pedido = crud.get_pedido(db, id=pedido_id)
    if db_pedido is None:
        raise HTTPException(status_code=404, detail="Pedido no encontrado")
    
    return db_pedido

@app.put("/pedidos/{pedido_id}/add_producto/{producto_id}", response_model=schemas.Pedido)
def add_producto_pedido(pedido_id: int, producto_id: int, db: Session = Depends(get_db)):
    db_pedido = crud.get_pedido(db, id=pedido_id)
    if db_pedido is None:
        raise HTTPException(status_code=404, detail="Pedido no encontrado")
    db_producto = crud.get_producto(db, id=producto_id)
    if db_producto is None:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    if(db_producto.stock == 0):
        raise HTTPException(status_code=404, detail="Producto agotado")
    db_producto.pedido_id = pedido_id
    db_producto.stock = db_producto.stock - 1
    db_pedido.productos.append(db_producto)
    db.commit()
    db.refresh(db_pedido)
    return db_pedido

@app.put("/pedidos/{pedido_id}/remove_producto/{producto_id}", response_model=schemas.Pedido)
def remove_producto_pedido(pedido_id: int, producto_id: int, db: Session = Depends(get_db)):
    db_pedido = crud.get_pedido(db, id=pedido_id)
    if db_pedido is None:
        raise HTTPException(status_code=404, detail="Pedido no encontrado")
    db_producto = crud.get_producto(db, id=producto_id)
    if db_producto is None:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    db_producto.pedido_id = None
    db_producto.stock = db_producto.stock + 1
    db_pedido.productos.remove(db_producto)
    db.commit()
    db.refresh(db_pedido)
    db.refresh(db_producto)
    return db_pedido


@app.put("/pedidos/{pedido_id}", response_model=schemas.Pedido)
def update_pedido(pedido_id: int, pedido: schemas.PedidoCreate, db: Session = Depends(get_db)):
    db_pedido = crud.get_pedido(db, id=pedido_id)
    if db_pedido is None:
        raise HTTPException(status_code=404, detail="Pedido no encontrado")
    db_pedido.cliente_id = pedido.cliente_id
    db_pedido.farmaceutico_id = pedido.farmaceutico_id
    db_pedido.productos = pedido.productos
    db_pedido.cantidad = pedido.cantidad
    db_pedido.total = pedido.total
    db_pedido.fecha = pedido.fecha
    db.commit()
    db.refresh(db_pedido)
    return db_pedido

@app.delete("/pedidos/{pedido_id}", response_model=schemas.Pedido)
def delete_pedido(pedido_id: int, db: Session = Depends(get_db)):
    db_pedido = crud.get_pedido(db, id=pedido_id)
    if db_pedido is None:
        raise HTTPException(status_code=404, detail="Pedido no encontrado")
    db.delete(db_pedido)
    db.commit()
    return db_pedido



