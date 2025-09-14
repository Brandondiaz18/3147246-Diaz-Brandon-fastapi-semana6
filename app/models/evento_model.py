from sqlalchemy import Column, Integer, String, Date, Float
from app.database import Base

class Evento(Base):
    __tablename__ = "eventos"

    id_evento = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    fecha = Column(Date, nullable=False)
    ubicacion = Column(String, nullable=False)
    tipo_evento = Column(String, nullable=False)
    precio = Column(Float, nullable=False)
    estado = Column(String, nullable=False)
