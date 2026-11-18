import json
from pathlib import Path

from scripts.generar_json_flutter import generar


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "cliente_flutter" / "assets" / "data" / "alcaldias.json"


def test_json_flutter_matches_deterministic_generation():
    generated = generar()
    stored = json.loads(OUTPUT.read_text(encoding="utf-8"))
    assert stored == generated


def test_json_flutter_has_16_unique_observed_alcaldias():
    data = json.loads(OUTPUT.read_text(encoding="utf-8"))
    assert len(data) == 16
    assert len({row["clave_alcaldia"] for row in data}) == 16
    assert len({row["alcaldia"] for row in data}) == 16
    assert all(row["periodo"] == "2020" for row in data)
    assert all(row["tipo_dato"] == "observado" for row in data)
    assert all(row["poblacion_total"] > 0 for row in data)
    assert all(row["poblacion_0_14"] <= row["poblacion_total"] for row in data)
    assert all(row["poblacion_60_mas"] <= row["poblacion_total"] for row in data)


def test_iztapalapa_matches_streamlit_source():
    data = {row["alcaldia"]: row for row in json.loads(OUTPUT.read_text(encoding="utf-8"))}
    iztapalapa = data["Iztapalapa"]
    assert iztapalapa["poblacion_total"] == 1835486
    assert iztapalapa["poblacion_0_4"] == 103148
    assert iztapalapa["poblacion_60_mas"] == 262064


def test_flutter_geometry_keys_match_indicators():
    indicators = json.loads(OUTPUT.read_text(encoding="utf-8"))
    geometry_path = ROOT / "cliente_flutter" / "assets" / "data" / "alcaldias.geojson"
    geometry = json.loads(geometry_path.read_text(encoding="utf-8"))
    indicator_keys = {row["clave_alcaldia"] for row in indicators}
    geometry_keys = {
        feature["properties"]["clave"]
        for feature in geometry["features"]
    }
    assert len(geometry["features"]) == 16
    assert geometry_keys == indicator_keys
