from fastapi import FastAPI
from app.database import Base, engine
from app.models import evento_model
from app.routers import evento_routes

# Crear las tablas en SQLite
Base.metadata.create_all(bind=engine)

app = FastAPI(title="API Eventos")

# Registrar el router
app.include_router(evento_routes.router)
