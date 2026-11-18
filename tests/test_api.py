from fastapi.testclient import TestClient

from api.main import app


client = TestClient(app)


def test_health():
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_matching_retorna_resultado_explicable():
    response = client.post("/api/matching", json={
        "tipo": "infantil",
        "inicio": "09:00",
        "fin": "12:00",
        "dias": ["lun", "mar"],
        "radio_km": 10,
    })
    assert response.status_code == 200
    body = response.json()
    assert body["demo"] is True
    assert body["results"]
    assert body["results"][0]["motivo"] in {
        "compatible",
        "sin_servicio_compatible",
        "sin_compatibilidad_horaria",
        "fuera_de_radio",
        "sin_cupo",
    }


def test_matching_rechaza_horario_invalido():
    response = client.post("/api/matching", json={
        "tipo": "infantil",
        "inicio": "18:00",
        "fin": "12:00",
        "dias": ["lun"],
        "radio_km": 10,
    })
    assert response.status_code == 422


def test_simulador_no_inventa_beneficio_neto():
    response = client.post("/api/simular", json={
        "numero_empleadas": 100,
        "salario_promedio": 12000,
        "bajas_anuales": 10,
        "reduccion_rotacion_pct": 20,
        "costo_reclutamiento": 6000,
        "costo_capacitacion": 4500,
        "costo_vacante_productividad": 16800,
        "costo_admin_transferencia": 3500,
        "dias_cotizados": 365,
        "factor_integracion_sbc": 1.049315,
        "tasa_imss_patronal": 0.204,
        "tasa_isn_cdmx": 0.04,
        "tasa_infonavit": 0.05,
        "costo_intervencion": None,
    })
    assert response.status_code == 200
    body = response.json()
    assert body["b2b"]["beneficio_neto"] is None
    assert body["b2g"]["total_impuestos"] == body["b2g"]["isn_impuesto"]
