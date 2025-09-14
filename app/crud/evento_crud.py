from sqlalchemy.orm import Session
from app.models import evento_model
from app.schemas import evento_schema

def crear_evento(db: Session, evento: evento_schema.EventoCreate):
    db_evento = evento_model.Evento(**evento.dict())
    db.add(db_evento)
    db.commit()
    db.refresh(db_evento)
    return db_evento

def obtener_eventos(db: Session, skip: int = 0, limit: int = 10):
    return db.query(evento_model.Evento).offset(skip).limit(limit).all()

def obtener_evento(db: Session, evento_id: int):
    return db.query(evento_model.Evento).filter(evento_model.Evento.id_evento == evento_id).first()

def actualizar_evento(db: Session, evento_id: int, evento: evento_schema.EventoCreate):
    db_evento = db.query(evento_model.Evento).filter(evento_model.Evento.id_evento == evento_id).first()
    if db_evento:
        for key, value in evento.dict().items():
            setattr(db_evento, key, value)
        db.commit()
        db.refresh(db_evento)
    return db_evento

def eliminar_evento(db: Session, evento_id: int):
    db_evento = db.query(evento_model.Evento).filter(evento_model.Evento.id_evento == evento_id).first()
    if db_evento:
        db.delete(db_evento)
        db.commit()
    return db_evento
