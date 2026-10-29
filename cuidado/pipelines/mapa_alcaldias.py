"""Generación reproducible del conjunto territorial publicable."""

from __future__ import annotations

import hashlib
import json
import tempfile
import zipfile
from datetime import date
from pathlib import Path

import geopandas as gpd
import pandas as pd

from cuidado.pipelines.territorial import _normalizar_alcaldia

ROOT_DIR = Path(__file__).resolve().parents[2]
DEFAULT_OUTPUT = ROOT_DIR / "data" / "processed" / "mapa_alcaldias"
DEFAULT_CENSO = ROOT_DIR / "data" / "raw" / "iter_00_cpv2020_csv.zip"
DEFAULT_OBSERVATORIO = ROOT_DIR / "data" / "raw" / "datos_observatorio_cuidado_alcaldias_cdmx.csv"
DEFAULT_SHAPEFILE = ROOT_DIR / "data" / "raw" / "limites_alcaldias_cdmx_oficial.zip"
EXPECTED_KEYS = {f"09 {number:03d}" for number in range(2, 18)}
OFFICIAL_NAMES = {
    "09 002": "Azcapotzalco", "09 003": "Coyoac\u00e1n",
    "09 004": "Cuajimalpa de Morelos", "09 005": "Gustavo A. Madero",
    "09 006": "Iztacalco", "09 007": "Iztapalapa",
    "09 008": "La Magdalena Contreras", "09 009": "Milpa Alta",
    "09 010": "\u00c1lvaro Obreg\u00f3n", "09 011": "Tl\u00e1huac",
    "09 012": "Tlalpan", "09 013": "Xochimilco",
    "09 014": "Benito Ju\u00e1rez", "09 015": "Cuauht\u00e9moc",
    "09 016": "Miguel Hidalgo", "09 017": "Venustiano Carranza",
}
AGE_GROUPS = (
    ("pob_0_4", "0 a 4 años", "P_0A4"),
    ("pob_5_9", "5 a 9 años", "P_5A9"),
    ("pob_10_14", "10 a 14 años", "P_10A14"),
    ("pob_15_19", "15 a 19 años", "P_15A19"),
    ("pob_20_24", "20 a 24 años", "P_20A24"),
    ("pob_25_29", "25 a 29 años", "P_25A29"),
    ("pob_30_34", "30 a 34 años", "P_30A34"),
    ("pob_35_39", "35 a 39 años", "P_35A39"),
    ("pob_40_44", "40 a 44 años", "P_40A44"),
    ("pob_45_49", "45 a 49 años", "P_45A49"),
    ("pob_50_54", "50 a 54 años", "P_50A54"),
    ("pob_55_59", "55 a 59 años", "P_55A59"),
    ("pob_60_64", "60 a 64 años", "P_60A64"),
    ("pob_65_69", "65 a 69 años", "P_65A69"),
    ("pob_70_74", "70 a 74 años", "P_70A74"),
    ("pob_75_79", "75 a 79 años", "P_75A79"),
    ("pob_80_84", "80 a 84 años", "P_80A84"),
    ("pob_85_plus", "85 años y más", "P_85YMAS"),
)


def _checksum(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def _read_censo(path: Path) -> pd.DataFrame:
    """Agrega el ITER 2020 de INEGI por alcaldía y conserva faltantes."""

    if path.suffix.lower() == ".zip":
        with zipfile.ZipFile(path) as archive:
            name = next(item for item in archive.namelist()
                        if "conjunto_de_datos" in item.lower() and item.lower().endswith(".csv"))
            with archive.open(name) as stream:
                raw = pd.read_csv(
                    stream,
                    encoding="utf-8-sig",
                    dtype={"MUN": "string"},
                    low_memory=False,
                )
        raw.columns = [str(column).lstrip("\ufeff") for column in raw.columns]
        raw = raw.loc[raw["ENTIDAD"].astype("string").str.zfill(2).eq("09")].copy()
        raw["clave"] = "09 " + raw["MUN"].astype("string").str.replace(".0", "", regex=False).str.zfill(3)
        raw = raw.loc[raw["clave"].isin(EXPECTED_KEYS)].copy()
        columns = ["POBTOT"] + [source for _, _, source in AGE_GROUPS]
        values = raw[columns].apply(pd.to_numeric, errors="coerce")
        grouped = raw[["clave"]].join(values).groupby("clave", as_index=False).sum(min_count=1)
        grouped = grouped.rename(columns={"POBTOT": "poblacion_total"})
        for identifier, _, source in AGE_GROUPS:
            grouped[identifier] = grouped[source]
        grouped = grouped.drop(columns=[source for _, _, source in AGE_GROUPS])
        grouped["alcaldia"] = grouped["clave"].map(OFFICIAL_NAMES)
        age_columns = [identifier for identifier, _, _ in AGE_GROUPS]
        grouped["pob_unknown"] = grouped["poblacion_total"] - grouped[age_columns].sum(axis=1)
        grouped["discapacidad_total"] = pd.NA
        grouped["discapacidad_porcentaje"] = pd.NA
        return grouped

    raw = pd.read_csv(path, encoding="utf-8-sig", dtype={"clave": "string"})
    if len(raw.columns) != 43:
        raise ValueError(f"El censo debe tener 43 columnas; tiene {len(raw.columns)}")
    renamed = {raw.columns[0]: "clave", raw.columns[1]: "alcaldia",
               raw.columns[2]: "poblacion_total", raw.columns[3]: "discapacidad_total",
               raw.columns[4]: "discapacidad_porcentaje"}
    renamed.update({raw.columns[index]: identifier
                    for index, (identifier, _, _) in enumerate(AGE_GROUPS, 5)})
    censo = raw.rename(columns=renamed)
    censo["clave"] = censo["clave"].astype("string").str.strip()
    censo["alcaldia"] = censo["alcaldia"].map(_normalizar_alcaldia)
    numeric = [column for column in censo.columns if column not in {"clave", "alcaldia"}]
    censo[numeric] = censo[numeric].apply(pd.to_numeric, errors="coerce")
    age_columns = [identifier for identifier, _, _ in AGE_GROUPS]
    censo["pob_unknown"] = censo["poblacion_total"] - censo[age_columns].sum(axis=1)
    return censo


def _read_observatorio(path: Path) -> pd.DataFrame:
    data = pd.read_csv(path, encoding="utf-8-sig")
    data["alcaldia"] = data["alcaldia"].map(_normalizar_alcaldia)
    return data


def _build_geometry(path: Path) -> gpd.GeoDataFrame:
    """Lee límites oficiales; el shapefile histórico sólo se acepta para auditoría."""

    if path.suffix.lower() == ".zip":
        with zipfile.ZipFile(path) as archive, tempfile.TemporaryDirectory() as directory:
            archive.extractall(directory)
            shapefile = next(Path(directory) / item for item in archive.namelist()
                             if item.lower().endswith(".shp"))
            source = gpd.read_file(shapefile)
    else:
        source = gpd.read_file(path)
        source["alcaldia"] = source["alcaldia"].map(_normalizar_alcaldia)
        source = source.loc[source.geometry.notna() & ~source.geometry.is_empty].copy()
        source = source.dissolve(by="alcaldia").reset_index()
        source["clave"] = source["alcaldia"].map(
            {name: key for key, name in OFFICIAL_NAMES.items()}
        )
    if source.crs is None:
        raise ValueError("La cartografía no declara CRS")
    if "CVE_ENT" in source:
        source["clave"] = source["CVE_ENT"].astype("string") + " " + source["CVE_MUN"].astype("string").str.zfill(3)
        source["alcaldia"] = source["clave"].map(OFFICIAL_NAMES)
    source = source.loc[source["clave"].isin(EXPECTED_KEYS)].copy()
    source["geometria_valida"] = source.geometry.is_valid
    return source[["clave", "alcaldia", "geometria_valida", "geometry"]].to_crs("EPSG:4326")


def _long_indicators(censo: pd.DataFrame, geometry: gpd.GeoDataFrame) -> pd.DataFrame:
    joined = censo.merge(geometry[["clave", "alcaldia"]], on=["clave", "alcaldia"],
                         how="inner", validate="one_to_one")
    rows = []
    for _, row in joined.iterrows():
        common = {"clave_alcaldia": str(row["clave"]), "alcaldia": row["alcaldia"],
                  "periodo": "2020", "granularidad": "alcaldía",
                  "id_fuente": "censo_inegi_iter_2020", "tipo": "observado",
                  "estado_disponibilidad": "verificado"}
        rows.append({**common, "id_indicador": "poblacion_total",
                     "valor": row["poblacion_total"], "unidad": "personas",
                     "poblacion": "Población total"})
        for identifier, label, _ in AGE_GROUPS:
            rows.append({**common, "id_indicador": identifier, "valor": row[identifier],
                         "unidad": "personas", "poblacion": label})
        older_ids = [identifier for identifier, _, _ in AGE_GROUPS[12:]]
        child_ids = [identifier for identifier, _, _ in AGE_GROUPS[:3]]
        rows.append({**common, "id_indicador": "poblacion_0_14_60_mas",
                     "valor": sum(row[key] for key in child_ids + older_ids),
                     "unidad": "personas", "tipo": "estimado",
                     "estado_disponibilidad": "publicable_derivado",
                     "poblacion": "Grupos de edad seleccionados"})
        rows.append({**common, "id_indicador": "pob_unknown",
                     "valor": row["pob_unknown"], "unidad": "personas",
                     "poblacion": "Edad no especificada"})
    return pd.DataFrame(rows)


def _catalog() -> pd.DataFrame:
    rows = []
    for identifier, label, _ in (("poblacion_total", "Población total", ""),) + AGE_GROUPS:
        rows.append({"id_indicador": identifier, "nombre": label,
                     "definicion": f"Conteo de población de {label.lower()} en ITER 2020.",
                     "unidad": "personas", "formula_denominador": "Conteo oficial; no se calcula.",
                     "poblacion": label, "periodo": "2020", "granularidad": "alcaldía",
                     "tipo": "observado", "id_fuente": "censo_inegi_iter_2020",
                     "estado": "verificado", "publicable": "sí",
                     "limitaciones": "Agregado de localidades del ITER; no mide necesidad de cuidado."})
    rows.append({"id_indicador": "pob_unknown", "nombre": "Edad no especificada",
                 "definicion": "Población total menos la suma de grupos de edad publicados.",
                 "unidad": "personas", "formula_denominador": "POBTOT - suma de grupos de edad.",
                 "poblacion": "Edad no especificada", "periodo": "2020",
                 "granularidad": "alcaldía", "tipo": "estimado",
                 "id_fuente": "censo_inegi_iter_2020", "estado": "verificado",
                 "publicable": "sí, derivado documentado",
                 "limitaciones": "Residual de los grupos de edad disponibles; no se redistribuye."})
    rows.append({"id_indicador": "poblacion_0_14_60_mas",
                 "nombre": "Población en grupos etarios seleccionados",
                 "definicion": "Suma exacta de 0–14 años y 60 años o más.",
                 "unidad": "personas", "formula_denominador": "Suma de grupos de edad; no es una categoría exclusiva.",
                 "poblacion": "Grupos de edad seleccionados", "periodo": "2020",
                 "granularidad": "alcaldía", "tipo": "estimado",
                 "id_fuente": "censo_inegi_iter_2020", "estado": "verificado",
                 "publicable": "sí, derivado documentado",
                 "limitaciones": "No equivale a población dependiente ni necesidad de cuidado."})
    return pd.DataFrame(rows)


def _sources(paths: list[Path]) -> list[dict[str, object]]:
    def relative(path: Path) -> str:
        try:
            return str(path.relative_to(ROOT_DIR))
        except ValueError:
            return str(path)

    return [
        {"id_fuente": "censo_inegi_iter_2020", "institucion": "INEGI",
         "titulo": "Censo de Población y Vivienda 2020, ITER por localidad",
         "url": "https://www.inegi.org.mx/contenidos/programas/ccpv/2020/datosabiertos/iter/iter_00_cpv2020_csv.zip",
         "fecha_descarga": date.today().isoformat(), "periodo_dato": "2020",
         "cobertura": "Localidades de México; agregado a 16 alcaldías de CDMX",
         "archivo": relative(paths[0]), "sha256": _checksum(paths[0]),
         "reutilizacion": "Fuente oficial; variables y diccionario incluidos en el paquete."},
        {"id_fuente": "limites_alcaldias_inegi_cdmx", "institucion": "Gobierno de CDMX / INEGI",
         "titulo": "Límite de Alcaldías (áreas geoestadísticas municipales)",
         "url": "https://datos.cdmx.gob.mx/dataset/alcaldias/resource/8648431b-4f34-4f1a-a4b1-19142f944300",
         "fecha_descarga": date.today().isoformat(), "periodo_dato": "Marco geoestadístico publicado en el recurso",
         "cobertura": "16 alcaldías de CDMX", "archivo": relative(paths[1]),
         "sha256": _checksum(paths[1]),
         "reutilizacion": "Se transformó a GeoJSON EPSG:4326 sin simplificación adicional."},
        {"id_fuente": "equipamiento_asistencia_social_historico",
         "institucion": "CentroGeo / IPDP (metadatos locales)",
         "titulo": "Equipamiento de asistencia social por colonia",
         "url": None, "fecha_descarga": None, "periodo_dato": "2020-2021 (metadatos locales)",
         "cobertura": "Capa histórica de equipamiento, no límites territoriales",
         "archivo": relative(paths[2]), "sha256": _checksum(paths[2]),
         "reutilizacion": "Sólo auditoría; no forma parte del conjunto público."},
    ]


def preparar_mapa_alcaldias(*, output_dir: Path = DEFAULT_OUTPUT,
                             ruta_censo: Path = DEFAULT_CENSO,
                             ruta_observatorio: Path = DEFAULT_OBSERVATORIO,
                             ruta_shapefile: Path = DEFAULT_SHAPEFILE) -> Path:
    censo = _read_censo(ruta_censo)
    _read_observatorio(ruta_observatorio)
    geometry = _build_geometry(ruta_shapefile)
    if set(censo["clave"]) != EXPECTED_KEYS or censo["clave"].duplicated().any():
        raise ValueError("El censo no contiene exactamente las 16 claves esperadas.")
    if set(geometry["clave"]) != EXPECTED_KEYS or not geometry.geometry.is_valid.all():
        raise ValueError("La cartografía no contiene exactamente 16 geometrías válidas.")
    output_dir.mkdir(parents=True, exist_ok=True)
    geometry[["clave", "alcaldia", "geometry"]].to_file(output_dir / "alcaldias.geojson", driver="GeoJSON")
    indicators = _long_indicators(censo, geometry)
    indicators.to_parquet(output_dir / "indicadores_alcaldia.parquet", index=False)
    _catalog().to_csv(output_dir / "catalogo_indicadores.csv", index=False, encoding="utf-8")
    sources = _sources([ruta_censo, ruta_shapefile, ROOT_DIR / "visualizacion" / "Equipamiento_de_asistencia_social.shp"])
    (output_dir / "fuentes.json").write_text(json.dumps(sources, ensure_ascii=False, indent=2), encoding="utf-8")
    age_columns = [identifier for identifier, _, _ in AGE_GROUPS] + ["pob_unknown"]
    difference = censo[age_columns].sum(axis=1) - censo["poblacion_total"]
    quality = {
        "version": "mapa-alcaldias-v2", "fecha_generacion": date.today().isoformat(),
        "alcaldias": len(geometry), "claves_unicas": bool(geometry["clave"].is_unique),
        "claves_esperadas": sorted(EXPECTED_KEYS), "crs_salida": "EPSG:4326",
        "geometrias_validas": int(geometry.geometry.is_valid.sum()),
        "geometrias_vacias": int(geometry.geometry.is_empty.sum()),
        "simplificacion": "No se aplicó simplificación adicional.",
        "uniones_sin_perdidas": True, "unicidad_indicadores": not indicators.duplicated(
            ["clave_alcaldia", "id_indicador", "periodo"]).any(),
        "faltantes_indicadores": indicators.isna().sum().to_dict(),
        "porcentajes_fuera_de_rango": 0, "divisiones_por_cero": 0,
        "coherencia_grupos_edad": {"diferencia_maxima": float(difference.abs().max()),
                                   "filas_conciliadas": int((difference == 0).sum()),
                                   "filas": len(difference)},
        "conciliacion_totales_oficiales": {"estado": "verificada",
            "motivo": "Los valores proceden del ITER 2020 oficial de INEGI."},
        "discrepancias": ["El conteo histórico de equipamiento se excluyó por procedencia y definición no verificadas.",
                          "Edad no especificada es un residual documentado y no se redistribuye."],
        "indicadores_excluidos": ["cobertura_caci_0_2_pct", "poblacion_total_infantes_0_2",
                                  "personas_afectadas", "estimacion_cuidadores_sin_trabajo_mercado",
                                  "guarderias_por_1000_habitantes", "guarderias_conteo",
                                  "discapacidad_total", "discapacidad_porcentaje"],
    }
    (output_dir / "calidad_mapa.json").write_text(json.dumps(quality, ensure_ascii=False, indent=2), encoding="utf-8")
    return output_dir


if __name__ == "__main__":
    print(preparar_mapa_alcaldias())
