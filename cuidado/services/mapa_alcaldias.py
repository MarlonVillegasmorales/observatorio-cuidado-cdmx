"""Consulta de los datos preparados para el explorador territorial."""

from __future__ import annotations

import json
from pathlib import Path

import geopandas as gpd
import pandas as pd
import streamlit as st

from cuidado.config import ROOT_DIR


MAPA_DIR = ROOT_DIR / "data" / "processed" / "mapa_alcaldias"
NOMBRES_ALCALDIAS = {
    "09 002": "Azcapotzalco",
    "09 003": "Coyoacán",
    "09 004": "Cuajimalpa de Morelos",
    "09 005": "Gustavo A. Madero",
    "09 006": "Iztacalco",
    "09 007": "Iztapalapa",
    "09 008": "La Magdalena Contreras",
    "09 009": "Milpa Alta",
    "09 010": "Álvaro Obregón",
    "09 011": "Tláhuac",
    "09 012": "Tlalpan",
    "09 013": "Xochimilco",
    "09 014": "Benito Juárez",
    "09 015": "Cuauhtémoc",
    "09 016": "Miguel Hidalgo",
    "09 017": "Venustiano Carranza",
}


def _archivos_mapa() -> tuple[Path, Path, Path, Path]:
    geojson = MAPA_DIR / "alcaldias.geojson"
    indicadores = MAPA_DIR / "indicadores_alcaldia.parquet"
    catalogo = MAPA_DIR / "catalogo_indicadores.csv"
    fuentes = MAPA_DIR / "fuentes.json"
    return geojson, indicadores, catalogo, fuentes


def _archivos_tabulares() -> tuple[Path, Path]:
    _, indicadores, catalogo, _ = _archivos_mapa()
    return indicadores, catalogo


def _firma_archivos_mapa() -> tuple[tuple[str, int, int], ...]:
    """Devuelve una firma barata para invalidar datos preparados modificados."""

    return tuple(
        (
            str(path),
            path.stat().st_mtime_ns if path.is_file() else 0,
            path.stat().st_size if path.is_file() else 0,
        )
        for path in _archivos_mapa()
    )


@st.cache_data(show_spinner="Cargando mapa territorial...")
def _cargar_mapa_alcaldias(
    version: str = "v3",
    firma: tuple[tuple[str, int, int], ...] | None = None,
) -> tuple[gpd.GeoDataFrame, pd.DataFrame, pd.DataFrame, list[dict]]:
    """Carga una vez los archivos preparados y los invalida si cambian."""

    del version
    if firma is None:
        firma = _firma_archivos_mapa()
    del firma
    geojson, indicadores, catalogo, fuentes = _archivos_mapa()
    faltantes = [str(path) for path in (geojson, indicadores, catalogo, fuentes) if not path.is_file()]
    if faltantes:
        raise FileNotFoundError(
            "Faltan archivos preparados del mapa territorial: " + ", ".join(faltantes)
        )
    geometria = gpd.read_file(geojson)
    datos = pd.read_parquet(indicadores)
    definiciones = pd.read_csv(catalogo)
    procedencia = json.loads(fuentes.read_text(encoding="utf-8"))
    return geometria, datos, definiciones, procedencia


def cargar_mapa_alcaldias(
    version: str = "v3",
) -> tuple[gpd.GeoDataFrame, pd.DataFrame, pd.DataFrame, list[dict]]:
    """Carga el mapa con invalidación por cambios en los archivos preparados."""

    return _cargar_mapa_alcaldias(version, _firma_archivos_mapa())


@st.cache_data(show_spinner="Cargando indicadores territoriales...")
def _cargar_indicadores_alcaldias(
    version: str = "v3",
    firma: tuple[tuple[str, int, int], ...] | None = None,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Carga sólo las tablas necesarias para comparar alcaldías."""

    del version
    if firma is None:
        firma = _firma_archivos_mapa()
    del firma
    indicadores_path, catalogo_path = _archivos_tabulares()
    faltantes = [str(path) for path in (indicadores_path, catalogo_path) if not path.is_file()]
    if faltantes:
        raise FileNotFoundError(
            "Faltan archivos tabulares del mapa territorial: " + ", ".join(faltantes)
        )
    return pd.read_parquet(indicadores_path), pd.read_csv(catalogo_path)


def cargar_indicadores_alcaldias(
    version: str = "v3",
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Carga indicadores y definiciones con invalidación por cambios en archivos."""

    return _cargar_indicadores_alcaldias(version, _firma_archivos_mapa())


# Compatibilidad con las pruebas y llamadas que omiten la capa de caché.
cargar_mapa_alcaldias.__wrapped__ = _cargar_mapa_alcaldias


def nombre_alcaldia(clave: str) -> str:
    """Devuelve el nombre de presentación para una clave territorial conocida."""

    return NOMBRES_ALCALDIAS.get(str(clave), "")


def claves_alcaldias(geometria: gpd.GeoDataFrame) -> list[str]:
    """Ordena claves como texto para conservar ceros y facilitar el selector."""

    return sorted(geometria["clave"].astype("string").tolist())


def indicadores_de_alcaldia(indicadores: pd.DataFrame, clave: str) -> pd.DataFrame:
    """Filtra por clave exacta; una clave desconocida devuelve una tabla vacía."""

    if not clave:
        return indicadores.iloc[0:0].copy()
    return indicadores.loc[indicadores["clave_alcaldia"].astype("string").eq(str(clave))].copy()


def indicadores_publicos(indicadores: pd.DataFrame, catalogo: pd.DataFrame) -> pd.DataFrame:
    """Conserva únicamente los indicadores con autorización explícita."""

    autorizados = catalogo.loc[
        catalogo["publicable"].astype("string").str.startswith("sí"),
        "id_indicador",
    ]
    return indicadores.loc[indicadores["id_indicador"].isin(autorizados)].copy()


def fila_indicador(
    indicadores: pd.DataFrame, clave: str, indicador: str
) -> pd.Series | None:
    """Obtiene un indicador exacto sin convertir ausencias en cero."""

    filas = indicadores_de_alcaldia(indicadores, clave)
    filas = filas.loc[filas["id_indicador"].eq(indicador)]
    if filas.empty:
        return None
    return filas.iloc[0]


COMPARISON_INDICATORS = {
    "pob_0_4": {
        "label": "Personas de 0 a 4 años",
        "numerator": ("pob_0_4",),
        "denominator": "poblacion_total",
    },
    "pob_60_plus": {
        "label": "Personas de 60 años o más",
        "numerator": (
            "pob_60_64",
            "pob_65_69",
            "pob_70_74",
            "pob_75_79",
            "pob_80_84",
            "pob_85_plus",
        ),
        "denominator": "poblacion_total",
    },
}


def _valor_indicadores(
    indicadores: pd.DataFrame,
    clave: str,
    ids: tuple[str, ...],
) -> float | None:
    filas = indicadores_de_alcaldia(indicadores, clave)
    valores = pd.to_numeric(
        filas.loc[filas["id_indicador"].isin(ids), "valor"], errors="coerce"
    )
    if len(valores) != len(ids) or valores.isna().any():
        return None
    return float(valores.sum())


def _proporcion(
    indicadores: pd.DataFrame,
    clave: str,
    numerator_ids: tuple[str, ...],
    denominator_id: str,
) -> tuple[float, float] | None:
    numerator = _valor_indicadores(indicadores, clave, numerator_ids)
    denominator = _valor_indicadores(indicadores, clave, (denominator_id,))
    if numerator is None or denominator is None or denominator <= 0:
        return None
    return numerator, denominator


def comparacion_composicion(
    indicadores: pd.DataFrame,
    clave_a: str,
    clave_b: str,
) -> pd.DataFrame:
    """Calcula proporciones comparables y una referencia ponderada de CDMX."""

    rows: list[dict[str, object]] = []
    for identifier, definition in COMPARISON_INDICATORS.items():
        numerator_ids = definition["numerator"]
        denominator_id = definition["denominator"]
        values = {
            clave: _proporcion(indicadores, clave, numerator_ids, denominator_id)
            for clave in (clave_a, clave_b)
        }
        all_rows = [
            _proporcion(indicadores, clave, numerator_ids, denominator_id)
            for clave in indicadores["clave_alcaldia"].astype("string").unique()
        ]
        if any(value is None for value in (*values.values(), *all_rows)):
            rows.append(
                {
                    "indicador": identifier,
                    "nombre": definition["label"],
                    "a": None,
                    "b": None,
                    "cdmx": None,
                    "diferencia_pp": None,
                }
            )
            continue
        pair_a = values[clave_a]
        pair_b = values[clave_b]
        if pair_a is None or pair_b is None:
            continue
        numerator_a, denominator_a = pair_a
        numerator_b, denominator_b = pair_b
        numerator_cdmx = sum(value[0] for value in all_rows if value is not None)
        denominator_cdmx = sum(value[1] for value in all_rows if value is not None)
        percentage_a = numerator_a / denominator_a * 100
        percentage_b = numerator_b / denominator_b * 100
        rows.append(
            {
                "indicador": identifier,
                "nombre": definition["label"],
                "a": percentage_a,
                "b": percentage_b,
                "cdmx": numerator_cdmx / denominator_cdmx * 100
                if denominator_cdmx > 0
                else None,
                "diferencia_pp": percentage_a - percentage_b,
            }
        )
    return pd.DataFrame(rows)
