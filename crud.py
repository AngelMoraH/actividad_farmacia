from sqlalchemy.orm import Session
import models
import schemas

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
