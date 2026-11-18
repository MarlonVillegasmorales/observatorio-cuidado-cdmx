import json
from pathlib import Path
from scripts.importar_directorio_infantil import PUBLICOS


def test_matriz_y_sedes_del_directorio():
    assets = Path(__file__).resolve().parents[1] / "cliente_flutter/assets/data"
    directorio = json.loads((assets / "directorio_infantil.json").read_text(encoding="utf8"))
    mapa = json.loads((assets / "alcaldias.geojson").read_text(encoding="utf8"))
    assert set(directorio) == {f["properties"]["clave"].replace(" ", "") for f in mapa["features"]}
    ids = set()
    for grupo in directorio.values():
        sedes = grupo["sedes"]
        assert len(sedes) == grupo["resumen"]["sedes_unicas"]
        for sede in sedes:
            assert sede["id"] not in ids
            ids.add(sede["id"])
            assert all(u["nombre"] and u["fuente_url"] for u in sede["unidades"])
            assert all(set(u) <= PUBLICOS for u in sede["unidades"])
        for campo, necesarios in {
            "con_horario": ("apertura", "cierre"),
            "con_capacidad_exacta": ("capacidad_exacta",),
            "con_rango_o_tope": ("capacidad_max",),
            "con_vacantes_fechadas": ("vacantes", "fecha_vacantes"),
        }.items():
            total = sum(any(all(k in u for k in necesarios) for u in s["unidades"]) for s in sedes)
            assert total == grupo["resumen"][campo]
