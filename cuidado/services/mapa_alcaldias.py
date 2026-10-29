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


@st.cache_data(show_spinner="Cargando mapa territorial...")
def cargar_mapa_alcaldias(version: str = "v3") -> tuple[gpd.GeoDataFrame, pd.DataFrame, pd.DataFrame, list[dict]]:
    """Carga una vez el GeoJSON, indicadores, catálogo y fuentes preparados."""

    del version
    geojson = MAPA_DIR / "alcaldias.geojson"
    indicadores = MAPA_DIR / "indicadores_alcaldia.parquet"
    catalogo = MAPA_DIR / "catalogo_indicadores.csv"
    fuentes = MAPA_DIR / "fuentes.json"
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
