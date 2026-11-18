"""Lectura y validación de los datos recibidos para la integración.

Este módulo solo consume archivos procesados. No descarga fuentes ni ejecuta
ETL durante el arranque de la aplicación.
"""

from __future__ import annotations

import re
import unicodedata
from pathlib import Path

import pandas as pd

from cuidado.config import ROOT_DIR


ALCALDIAS_CDMX = frozenset(
    {
        "Alvaro Obregon",
        "Azcapotzalco",
        "Benito Juarez",
        "Coyoacan",
        "Cuajimalpa de Morelos",
        "Cuauhtemoc",
        "Gustavo A. Madero",
        "Iztacalco",
        "Iztapalapa",
        "La Magdalena Contreras",
        "Miguel Hidalgo",
        "Milpa Alta",
        "Tlahuac",
        "Tlalpan",
        "Venustiano Carranza",
        "Xochimilco",
    }
)

ENTREGAS_DIR = ROOT_DIR / "ETL_Datos"
CONAPO_PATH = ENTREGAS_DIR / "02_Datos_Procesados" / "CONAPO_CDMX_PROCESADO_2021_2030.csv"
MOVILIDAD_PATH = ENTREGAS_DIR / "02_Datos_Procesados" / "MOVILIDAD_CDMX_RUTAS_PARADAS.csv"
EMPRESAS_PATH = ENTREGAS_DIR / "02_Datos_Procesados" / "EMPRESAS_B2B2C_CDMX.csv"


def _normalizar_texto(value: object) -> str:
    text = unicodedata.normalize("NFKD", str(value))
    text = "".join(char for char in text if not unicodedata.combining(char))
    return re.sub(r"\s+", " ", text).strip().lower()


_ALCALDIAS_NORMALIZADAS = {
    _normalizar_texto(nombre): nombre for nombre in ALCALDIAS_CDMX
}


def _canonicalizar_alcaldias(series: pd.Series) -> pd.Series:
    canonical = series.map(lambda value: _ALCALDIAS_NORMALIZADAS.get(_normalizar_texto(value)))
    if canonical.isna().any():
        desconocidas = sorted(series[canonical.isna()].dropna().astype(str).unique())
        raise ValueError(f"Alcaldías fuera del catálogo CDMX: {desconocidas}")
    return canonical


def _read_csv(path: Path, **kwargs: object) -> pd.DataFrame:
    if not path.is_file():
        raise FileNotFoundError(f"No existe el archivo procesado requerido: {path}")
    return pd.read_csv(path, encoding="utf-8-sig", **kwargs)


def cargar_conapo(path: Path = CONAPO_PATH) -> pd.DataFrame:
    """Carga proyecciones CONAPO conservando periodo y granularidad."""

    data = _read_csv(path)
    required = {"CLAVE", "NOM_MUN", "SEXO", "ANO", "POB_TOTAL"}
    missing = required.difference(data.columns)
    if missing:
        raise ValueError(f"CONAPO carece de columnas requeridas: {sorted(missing)}")
    data["CLAVE"] = data["CLAVE"].astype("string").str.replace(r"\.0$", "", regex=True).str.zfill(4)
    data["ANO"] = pd.to_numeric(data["ANO"], errors="raise").astype("int64")
    data["alcaldia"] = _canonicalizar_alcaldias(data["NOM_MUN"])
    if not data["ANO"].between(2021, 2030).all():
        raise ValueError("CONAPO contiene periodos fuera de 2021-2030")
    if data["alcaldia"].nunique() != 16:
        raise ValueError("CONAPO no contiene las 16 alcaldías de CDMX")
    if data.duplicated(["CLAVE", "ANO", "SEXO"]).any():
        raise ValueError("CONAPO contiene claves territoriales duplicadas")
    data["es_proyeccion"] = True
    data["tipo_dato"] = "proyeccion"
    return data


def _validar_tr13_semovi(data: pd.DataFrame) -> None:
    route = data["route_short_name"].astype("string").str.upper().str.strip()
    agency = data["agency_name"].astype("string").str.upper().str.strip()
    inconsistency = data[route.eq("TR13") & agency.str.contains("SEMOVI", na=False)]
    if not inconsistency.empty:
        raise ValueError(
            "Se detectó la relación TR13/SEMOVI en movilidad; requiere revisar "
            "la fuente original y no se corregirá silenciosamente."
        )


def cargar_movilidad(path: Path = MOVILIDAD_PATH) -> pd.DataFrame:
    """Carga relaciones ruta-parada; no las interpreta como tiempos de viaje."""

    data = _read_csv(path, dtype={"route_id": "string", "stop_id": "string", "agency_id": "string"})
    required = {
        "route_id",
        "agency_id",
        "agency_name",
        "route_short_name",
        "route_long_name",
        "stop_id",
        "stop_name",
        "stop_lat",
        "stop_lon",
    }
    missing = required.difference(data.columns)
    if missing:
        raise ValueError(f"Movilidad carece de columnas requeridas: {sorted(missing)}")
    data["stop_lat"] = pd.to_numeric(data["stop_lat"], errors="raise")
    data["stop_lon"] = pd.to_numeric(data["stop_lon"], errors="raise")
    if data[list(required)].isna().any().any():
        raise ValueError("Movilidad contiene nulos en columnas de relación")
    if data.duplicated(["route_id", "stop_id"]).any():
        raise ValueError("Movilidad contiene relaciones ruta-parada duplicadas")
    _validar_tr13_semovi(data)
    data["representa_tiempo_viaje"] = False
    return data


def cargar_empresas(path: Path = EMPRESAS_PATH) -> pd.DataFrame:
    """Carga la plantilla empresarial y marca explícitamente su carácter sintético."""

    data = _read_csv(path, dtype={"d_codigo": "string"})
    required = {"d_codigo", "D_mnpio", "empresa_id", "nombre_empresa"}
    missing = required.difference(data.columns)
    if missing:
        raise ValueError(f"Empresas carece de columnas requeridas: {sorted(missing)}")
    data["d_codigo"] = data["d_codigo"].astype("string").str.strip().str.zfill(5)
    if not data["d_codigo"].str.fullmatch(r"\d{5}").all():
        raise ValueError("Los códigos postales deben ser texto de cinco dígitos")
    data["alcaldia"] = _canonicalizar_alcaldias(data["D_mnpio"])
    if data["alcaldia"].nunique() != 16:
        raise ValueError("Empresas no contiene representación de las 16 alcaldías")
    if data["empresa_id"].duplicated().any():
        raise ValueError("Empresas contiene identificadores duplicados")
    data["es_simulada"] = True
    data["tipo_dato"] = "sintetico"
    return data


def validar_entregas() -> dict[str, int]:
    """Valida los tres procesados disponibles sin ejecutar ningún ETL."""

    conapo = cargar_conapo()
    movilidad = cargar_movilidad()
    empresas = cargar_empresas()
    return {
        "conapo_filas": len(conapo),
        "conapo_alcaldias": conapo["alcaldia"].nunique(),
        "movilidad_filas": len(movilidad),
        "movilidad_rutas": movilidad["route_id"].nunique(),
        "movilidad_paradas": movilidad["stop_id"].nunique(),
        "empresas_filas": len(empresas),
        "empresas_alcaldias": empresas["alcaldia"].nunique(),
    }
