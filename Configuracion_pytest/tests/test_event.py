# tests/test_event.py
import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


class TestEventAPI:
    """
    Tests específicos para el dominio de Eventos - FICHA 3147246
    """

    def test_create_event_success(self):
        """Crear un evento válido"""
        data = {
            "nombre": "Conferencia de Tecnología",
            "fecha": "2025-09-30",
            "lugar": "Centro de Convenciones Bogotá",
            "capacidad": 300,
            "descripcion": "Evento sobre IA y ciberseguridad"
        }
        response = client.post("/event_eventos/", json=data, headers={"x-role": "admin"})
        assert response.status_code == 201
        result = response.json()
        assert result["nombre"] == data["nombre"]
        assert result["capacidad"] == 300
        assert "id" in result

    def test_create_event_invalid_capacity(self):
        """Validar que no se pueda crear evento con capacidad negativa"""
        data = {
            "nombre": "Festival de Música",
            "fecha": "2025-10-15",
            "lugar": "Parque Central",
            "capacidad": -50,  # ❌ no permitido
            "descripcion": "Evento al aire libre"
        }
        response = client.post("/event_eventos/", json=data, headers={"x-role": "admin"})
        assert response.status_code == 422

    def test_get_event_by_id(self):
        """Crear y luego consultar un evento por ID"""
        data = {
            "nombre": "Hackathon 2025",
            "fecha": "2025-11-20",
            "lugar": "Campus Universitario",
            "capacidad": 200,
            "descripcion": "Competencia de desarrollo de software"
        }
        create = client.post("/event_eventos/", json=data, headers={"x-role": "admin"})
        event_id = create.json()["id"]

        response = client.get(f"/event_eventos/{event_id}")
        assert response.status_code == 200
        assert response.json()["id"] == event_id

    def test_get_event_not_found(self):
        """Consultar evento inexistente debe devolver 404"""
        response = client.get("/event_eventos/99999")
        assert response.status_code == 404
        assert "evento" in response.json()["detail"].lower()

    def test_update_event(self):
        """Actualizar un evento existente"""
        data = {
            "nombre": "Feria de Innovación",
            "fecha": "2025-12-01",
            "lugar": "Plaza Mayor",
            "capacidad": 150,
            "descripcion": "Exposición de proyectos tecnológicos"
        }
        create = client.post("/event_eventos/", json=data, headers={"x-role": "admin"})
        event_id = create.json()["id"]

        update_data = {**data, "capacidad": 400, "descripcion": "Actualizado"}
        response = client.put(f"/event_eventos/{event_id}", json=update_data, headers={"x-role": "admin"})

        assert response.status_code == 200
        result = response.json()
        assert result["capacidad"] == 400
        assert result["descripcion"] == "Actualizado"

    def test_delete_event(self):
        """Eliminar un evento y verificar que ya no exista"""
        data = {
            "nombre": "Reunión Empresarial",
            "fecha": "2025-09-25",
            "lugar": "Hotel Hilton",
            "capacidad": 80,
            "descripcion": "Networking para emprendedores"
        }
        create = client.post("/event_eventos/", json=data, headers={"x-role": "admin"})
        event_id = create.json()["id"]

        response = client.delete(f"/event_eventos/{event_id}", headers={"x-role": "admin"})
        assert response.status_code == 200

        # Verificar que ya no existe
        check = client.get(f"/event_eventos/{event_id}")
        assert check.status_code == 404


# ===================== NUEVOS TESTS PARA PRÁCTICA 21 (AUTENTICACIÓN) =====================

def test_create_event_forbidden():
    """Debe devolver 403 si un usuario sin rol admin intenta crear evento"""
    data = {
        "nombre": "Evento No Autorizado",
        "fecha": "2025-09-20",
        "lugar": "Auditorio",
        "capacidad": 100,
        "descripcion": "Debe fallar"
    }
    response = client.post("/event_eventos/", json=data, headers={"x-role": "user"})
    assert response.status_code == 403
    assert response.json()["detail"] == "No autorizado"


def test_update_event_forbidden():
    """Debe devolver 403 si un usuario sin rol admin intenta actualizar evento"""
    data = {
        "nombre": "Evento Admin",
        "fecha": "2025-09-25",
        "lugar": "Hotel",
        "capacidad": 50,
        "descripcion": "Prueba"
    }
    # Crear como admin
    create = client.post("/event_eventos/", json=data, headers={"x-role": "admin"})
    event_id = create.json()["id"]

    # Intentar actualizar como usuario normal
    response = client.put(f"/event_eventos/{event_id}", json={"nombre": "Hack"}, headers={"x-role": "user"})
    assert response.status_code == 403


def test_delete_event_forbidden():
    """Debe devolver 403 si un usuario sin rol admin intenta borrar evento"""
    data = {
        "nombre": "Evento para Borrar",
        "fecha": "2025-09-30",
        "lugar": "Auditorio",
        "capacidad": 60,
        "descripcion": "Prueba delete"
    }
    create = client.post("/event_eventos/", json=data, headers={"x-role": "admin"})
    event_id = create.json()["id"]

    # Intentar borrar como usuario normal
    response = client.delete(f"/event_eventos/{event_id}", headers={"x-role": "user"})
    assert response.status_code == 403
