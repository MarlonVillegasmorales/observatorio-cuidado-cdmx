"""Simulador B2B/B2G validado y reutilizable.

Los resultados son escenarios sintéticos. No estiman impacto observado ni
calculan beneficio neto cuando no se proporciona un costo de intervención.
"""

from __future__ import annotations

import math
from pathlib import Path
from typing import Any, Mapping

import pandas as pd

from cuidado.config import ROOT_DIR


SCENARIOS_PATH = ROOT_DIR / "data" / "processed" / "simulador_b2b_b2g_parametros.csv"
REQUIRED_NUMERIC = (
    "numero_empleadas",
    "salario_promedio",
    "bajas_anuales",
    "reduccion_rotacion_pct",
    "costo_reclutamiento",
    "costo_capacitacion",
    "costo_vacante_productividad",
    "costo_admin_transferencia",
    "dias_cotizados",
    "factor_integracion_sbc",
    "tasa_imss_patronal",
    "tasa_isn_cdmx",
    "tasa_infonavit",
)


def _number(row: Mapping[str, Any], name: str) -> float:
    value = row.get(name)
    if value is None or pd.isna(value):
        raise ValueError(f"El escenario no contiene {name}")
    result = float(value)
    if not math.isfinite(result):
        raise ValueError(f"{name} debe ser finito")
    return result


def validar_escenario(row: Mapping[str, Any]) -> None:
    values = {name: _number(row, name) for name in REQUIRED_NUMERIC}
    positive = (
        "numero_empleadas",
        "salario_promedio",
        "costo_reclutamiento",
        "costo_capacitacion",
        "costo_vacante_productividad",
        "costo_admin_transferencia",
        "factor_integracion_sbc",
    )
    for name in positive:
        if values[name] <= 0:
            raise ValueError(f"{name} debe ser mayor que cero")
    for name in ("bajas_anuales", "dias_cotizados"):
        if values[name] < 0:
            raise ValueError(f"{name} no puede ser negativo")
    if not 1 <= values["dias_cotizados"] <= 366:
        raise ValueError("dias_cotizados debe estar entre 1 y 366")
    if not 0 <= values["reduccion_rotacion_pct"] <= 100:
        raise ValueError("reduccion_rotacion_pct debe estar entre 0 y 100")
    for name in ("tasa_imss_patronal", "tasa_isn_cdmx", "tasa_infonavit"):
        if not 0 <= values[name] <= 1:
            raise ValueError(f"{name} debe estar entre 0 y 1")


def simular_b2b(row: Mapping[str, Any]) -> dict[str, float | None]:
    """Calcula ahorro bruto por rotación y deja beneficio neto explícito."""

    validar_escenario(row)
    costo_por_baja = sum(_number(row, name) for name in (
        "costo_reclutamiento",
        "costo_capacitacion",
        "costo_vacante_productividad",
        "costo_admin_transferencia",
    ))
    bajas = _number(row, "bajas_anuales")
    evitadas = bajas * _number(row, "reduccion_rotacion_pct") / 100
    ahorro = evitadas * costo_por_baja
    costo_intervencion = row.get("costo_intervencion")
    if costo_intervencion is not None and not pd.isna(costo_intervencion):
        costo_intervencion = float(costo_intervencion)
        if not math.isfinite(costo_intervencion) or costo_intervencion < 0:
            raise ValueError("costo_intervencion debe ser finito y no negativo")
        beneficio_neto: float | None = ahorro - costo_intervencion
    else:
        costo_intervencion = None
        beneficio_neto = None
    return {
        "costo_total_rotacion": round(bajas * costo_por_baja, 2),
        "bajas_evitadas": round(evitadas, 2),
        "ahorro_bruto": round(ahorro, 2),
        "costo_intervencion": costo_intervencion,
        "beneficio_neto": None if beneficio_neto is None else round(beneficio_neto, 2),
    }


def simular_b2g(row: Mapping[str, Any]) -> dict[str, float]:
    """Separa impuesto ISN de aportaciones patronales."""

    validar_escenario(row)
    salario_anual = _number(row, "salario_promedio") * 12
    base_nominal = salario_anual * _number(row, "numero_empleadas")
    base_sbc = base_nominal * _number(row, "factor_integracion_sbc")
    dias_factor = _number(row, "dias_cotizados") / 365
    base_nominal *= dias_factor
    base_sbc *= dias_factor
    imss = base_sbc * _number(row, "tasa_imss_patronal")
    isn = base_nominal * _number(row, "tasa_isn_cdmx")
    infonavit = base_sbc * _number(row, "tasa_infonavit")
    return {
        "imss_patronal": round(imss, 2),
        "isn_impuesto": round(isn, 2),
        "infonavit_aportacion": round(infonavit, 2),
        "total_impuestos": round(isn, 2),
        "total_aportaciones": round(imss + infonavit, 2),
        "total_flujos_publicos": round(imss + isn + infonavit, 2),
    }


def simular_escenario(row: Mapping[str, Any]) -> dict[str, Any]:
    resultado = dict(row)
    resultado.update({f"b2b_{key}": value for key, value in simular_b2b(row).items()})
    resultado.update({f"b2g_{key}": value for key, value in simular_b2g(row).items()})
    return resultado


def cargar_escenarios(path: Path = SCENARIOS_PATH) -> pd.DataFrame:
    if not path.is_file():
        raise FileNotFoundError(f"No existe el CSV canónico de escenarios: {path}")
    data = pd.read_csv(path, encoding="utf-8-sig")
    if len(data) != 30:
        raise ValueError(f"Se esperaban 30 escenarios y se recibieron {len(data)}")
    if data["escenario_id"].duplicated().any():
        raise ValueError("Los escenarios tienen identificadores duplicados")
    for _, row in data.iterrows():
        validar_escenario(row)
    return data


def ejecutar_escenarios(path: Path = SCENARIOS_PATH) -> pd.DataFrame:
    data = cargar_escenarios(path)
    return pd.DataFrame(simular_escenario(row) for row in data.to_dict("records"))
