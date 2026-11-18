from __future__ import annotations

import os
from datetime import time
from typing import Literal

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from cuidado.services.simulacion import ejecutar_busqueda
from cuidado.services.simulador_b2b_b2g import simular_b2b, simular_b2g


DEFAULT_ORIGINS = (
    "http://localhost:8080",
    "http://127.0.0.1:8080",
    "https://proyecto-cuidado-21dcb--revision-integracion-9yzc3a0x.web.app",
    "https://proyecto-cuidado-21dcb.web.app",
)
allowed_origins = tuple(
    origin.strip()
    for origin in os.getenv("OBSERVATORIO_CORS_ORIGINS", ",".join(DEFAULT_ORIGINS)).split(",")
    if origin.strip()
)

app = FastAPI(title="API del Observatorio del Cuidado CDMX", version="1.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=list(allowed_origins),
    allow_credentials=False,
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type"],
)


class MatchingRequest(BaseModel):
    tipo: Literal["infantil", "mayores"]
    inicio: str = Field(description="Hora local HH:MM")
    fin: str = Field(description="Hora local HH:MM")
    dias: list[Literal["lun", "mar"]] = Field(min_length=1)
    radio_km: float = Field(default=10, gt=0, le=20)


class SimulatorRequest(BaseModel):
    numero_empleadas: float = Field(gt=0)
    salario_promedio: float = Field(gt=0)
    bajas_anuales: float = Field(ge=0)
    reduccion_rotacion_pct: float = Field(ge=0, le=100)
    costo_reclutamiento: float = Field(gt=0)
    costo_capacitacion: float = Field(gt=0)
    costo_vacante_productividad: float = Field(gt=0)
    costo_admin_transferencia: float = Field(gt=0)
    dias_cotizados: float = Field(ge=1, le=366)
    factor_integracion_sbc: float = Field(gt=0)
    tasa_imss_patronal: float = Field(ge=0, le=1)
    tasa_isn_cdmx: float = Field(ge=0, le=1)
    tasa_infonavit: float = Field(ge=0, le=1)
    costo_intervencion: float | None = Field(default=None, ge=0)


@app.get("/api/health")
def health() -> dict[str, str]:
    return {"status": "ok", "service": "observatorio-cdmx"}


@app.post("/api/matching")
def matching(request: MatchingRequest) -> dict[str, object]:
    try:
        inicio = time.fromisoformat(request.inicio)
        fin = time.fromisoformat(request.fin)
        results = ejecutar_busqueda(
            request.tipo,
            inicio,
            fin,
            request.dias,
            request.radio_km,
        )
    except (TypeError, ValueError) as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    return {"demo": True, "radio_km": request.radio_km, "results": results}


@app.post("/api/simular")
def simular(request: SimulatorRequest) -> dict[str, object]:
    row = request.model_dump()
    try:
        b2b = simular_b2b(row)
        b2g = simular_b2g(row)
    except (TypeError, ValueError) as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    return {
        "demo": True,
        "b2b": b2b,
        "b2g": b2g,
    }
