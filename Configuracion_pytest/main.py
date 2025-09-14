# main.py
from fastapi import FastAPI, HTTPException, Header, status

app = FastAPI(title="API de Eventos - FICHA 3147246")

fake_db = []
counter = 1


def check_admin(x_role: str):
    """Función para validar si el usuario es administrador"""
    if x_role != "admin":
        raise HTTPException(status_code=403, detail="No autorizado")


@app.post("/event_eventos/", status_code=status.HTTP_201_CREATED)
def create_event(evento: dict, x_role: str = Header(default="user")):
    check_admin(x_role)
    global counter
    if evento.get("capacidad", 0) < 0:
        raise HTTPException(status_code=422, detail="La capacidad no puede ser negativa")

    evento["id"] = counter
    counter += 1
    fake_db.append(evento)
    return evento


@app.get("/event_eventos/{evento_id}")
def get_event(evento_id: int):
    for e in fake_db:
        if e["id"] == evento_id:
            return e
    raise HTTPException(status_code=404, detail="Evento no encontrado")


@app.put("/event_eventos/{evento_id}")
def update_event(evento_id: int, updated: dict, x_role: str = Header(default="user")):
    check_admin(x_role)
    for e in fake_db:
        if e["id"] == evento_id:
            e.update(updated)
            return e
    raise HTTPException(status_code=404, detail="Evento no encontrado")


@app.delete("/event_eventos/{evento_id}")
def delete_event(evento_id: int, x_role: str = Header(default="user")):
    check_admin(x_role)
    for e in fake_db:
        if e["id"] == evento_id:
            fake_db.remove(e)
            return {"message": "Evento eliminado"}
    raise HTTPException(status_code=404, detail="Evento no encontrado")


@app.get("/")
def root():
    return {"message": "API de eventos funcionando 🚀"}
