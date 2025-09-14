from pydantic import BaseModel
from datetime import date

class EventoBase(BaseModel):
    nombre: str
    fecha: date
    ubicacion: str
    tipo_evento: str
    precio: float
    estado: str

class EventoCreate(EventoBase):
    pass

class Evento(EventoBase):
    id_evento: int

    class Config:
        from_attributes = True  # antes era orm_mode en Pydantic v1
