"""Genera el JSON territorial consumido por Flutter desde indicadores preparados."""

from __future__ import annotations

import json
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data" / "processed" / "mapa_alcaldias" / "indicadores_alcaldia.parquet"
OUTPUT = ROOT / "cliente_flutter" / "assets" / "data" / "alcaldias.json"

OFFICIAL_NAMES = {
    "09 002": "Azcapotzalco",
    "09 014": "Benito Juárez",
    "09 003": "Coyoacán",
    "09 004": "Cuajimalpa de Morelos",
    "09 015": "Cuauhtémoc",
    "09 005": "Gustavo A. Madero",
    "09 006": "Iztacalco",
    "09 007": "Iztapalapa",
    "09 008": "La Magdalena Contreras",
    "09 016": "Miguel Hidalgo",
    "09 009": "Milpa Alta",
    "09 012": "Tlalpan",
    "09 010": "Álvaro Obregón",
    "09 011": "Tláhuac",
    "09 017": "Venustiano Carranza",
    "09 013": "Xochimilco",
}

OLDER = ("pob_60_64", "pob_65_69", "pob_70_74", "pob_75_79", "pob_80_84", "pob_85_plus")
CHILDREN = ("pob_0_4", "pob_5_9", "pob_10_14")
REQUIRED = ("poblacion_total", "pob_0_4", *OLDER, *CHILDREN)


def generar() -> list[dict[str, object]]:
    if not SOURCE.is_file():
        raise FileNotFoundError(f"No existe el dataset preparado: {SOURCE}")

    data = pd.read_parquet(SOURCE)
    required_columns = {"clave_alcaldia", "alcaldia", "periodo", "id_indicador", "valor", "unidad", "tipo"}
    missing = required_columns.difference(data.columns)
    if missing:
        raise ValueError(f"Faltan columnas territoriales: {sorted(missing)}")

    pivot = data.pivot_table(
        index=["clave_alcaldia", "periodo"],
        columns="id_indicador",
        values="valor",
        aggfunc="first",
    )
    if len(pivot) != 16:
        raise ValueError(f"Se esperaban 16 alcaldías y se encontraron {len(pivot)}")

    result: list[dict[str, object]] = []
    for (clave, periodo), row in pivot.sort_index().iterrows():
        clave = str(clave).strip()
        if clave not in OFFICIAL_NAMES:
            raise ValueError(f"Clave territorial no reconocida: {clave}")
        missing_values = [name for name in REQUIRED if pd.isna(row.get(name))]
        if missing_values:
            raise ValueError(f"Valores faltantes en {OFFICIAL_NAMES[clave]}: {missing_values}")

        total = int(row["poblacion_total"])
        child_14 = sum(int(row[name]) for name in CHILDREN)
        older = sum(int(row[name]) for name in OLDER)
        if child_14 > total or older > total:
            raise ValueError(f"Grupo mayor que población total en {OFFICIAL_NAMES[clave]}")

        result.append({
            "clave_alcaldia": clave,
            "alcaldia": OFFICIAL_NAMES[clave],
            "periodo": str(periodo),
            "poblacion_total": total,
            "poblacion_0_4": int(row["pob_0_4"]),
            "poblacion_0_14": child_14,
            "poblacion_60_mas": older,
            "fuente": "INEGI, Censo 2020 (ITER)",
            "tipo_dato": "observado",
        })

    if len({item["clave_alcaldia"] for item in result}) != 16:
        raise ValueError("Las claves territoriales deben ser únicas")
    if len({item["alcaldia"] for item in result}) != 16:
        raise ValueError("Los nombres de alcaldía deben ser únicos")
    return result


def main() -> None:
    result = generar()
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    print(f"Generado {OUTPUT.relative_to(ROOT)}: {len(result)} alcaldías")


if __name__ == "__main__":
    main()
