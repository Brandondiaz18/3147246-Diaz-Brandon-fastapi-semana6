from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas import evento_schema
from app.crud import evento_crud
from app.database import SessionLocal

router = APIRouter(prefix="/eventos", tags=["Eventos"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=evento_schema.Evento)
def crear_evento(evento: evento_schema.EventoCreate, db: Session = Depends(get_db)):
    return evento_crud.crear_evento(db, evento)

@router.get("/", response_model=list[evento_schema.Evento])
def obtener_eventos(db: Session = Depends(get_db)):
    return evento_crud.obtener_eventos(db)

@router.get("/{evento_id}", response_model=evento_schema.Evento)
def obtener_evento(evento_id: int, db: Session = Depends(get_db)):
    db_evento = evento_crud.obtener_evento(db, evento_id)
    if not db_evento:
        raise HTTPException(status_code=404, detail="Evento no encontrado")
    return db_evento

@router.put("/{evento_id}", response_model=evento_schema.Evento)
def actualizar_evento(evento_id: int, evento: evento_schema.EventoCreate, db: Session = Depends(get_db)):
    db_evento = evento_crud.actualizar_evento(db, evento_id, evento)
    if not db_evento:
        raise HTTPException(status_code=404, detail="Evento no encontrado")
    return db_evento

@router.delete("/{evento_id}")
def eliminar_evento(evento_id: int, db: Session = Depends(get_db)):
    db_evento = evento_crud.eliminar_evento(db, evento_id)
    if not db_evento:
        raise HTTPException(status_code=404, detail="Evento no encontrado")
    return {"ok": True, "message": "Evento eliminado"}
