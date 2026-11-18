"""Importa el ZIP documental del observatorio. Uso: python scripts/importar_directorio_infantil.py archivo.zip"""
import csv
import io
import json
import sys
from pathlib import Path
from zipfile import ZipFile

ASSETS = Path(__file__).resolve().parents[1] / "cliente_flutter/assets/data"
PUBLICOS = frozenset("""
    red nombre domicilio periodo_fuente fuente_url clave_origen apertura cierre
    apertura_extra cierre_extra periodo_horario capacidad_exacta capacidad_min
    capacidad_max periodo_capacidad fuente_capacidad_url vacantes fecha_vacantes
    fuente_vacantes_url nota
""".split())


def preparar(paquete):
    def tabla(nombre):
        with paquete.open(nombre + ".csv") as data:
            return list(csv.DictReader(io.TextIOWrapper(data, encoding="utf-8-sig")))

    geometrias = json.loads((ASSETS / "alcaldias.geojson").read_text(encoding="utf8"))
    nombres = {f["properties"]["clave"].replace(" ", ""): f["properties"]["alcaldia"]
               for f in geometrias["features"]}
    grupos = {}
    for fila in tabla("matriz_16_alcaldias"):
        clave = fila["cvegeo"]
        grupos[clave] = {"nombre": nombres[clave], "resumen": {
            k: int(fila[k]) for k in ("sedes_unicas", "con_horario", "con_capacidad_exacta",
                                       "con_rango_o_tope", "con_vacantes_fechadas")}, "sedes": []}
    por_id = {}
    for fila in tabla("directorio"):
        clave = fila["cvegeo"]
        identidad = fila["id_sede"]
        if identidad not in por_id:
            sede = {"id": identidad, "unidades": []}
            grupos[clave]["sedes"].append(sede)
            por_id[identidad] = sede
        sede = por_id[identidad]
        if fila["latitud"] and fila["longitud"] and "punto" not in sede:
            sede["punto"] = [float(fila["latitud"]), float(fila["longitud"])]
        sede["unidades"].append({k: v for k, v in fila.items() if v and k in PUBLICOS})
    if set(grupos) != set(nombres) or any(len(g["sedes"]) != g["resumen"]["sedes_unicas"] for g in grupos.values()):
        raise ValueError("La matriz territorial no coincide con el directorio")
    return grupos


if __name__ == "__main__":
    with ZipFile(sys.argv[1]) as archivo:
        grupos = preparar(archivo)
    destino = ASSETS / "directorio_infantil.json"
    destino.write_text(json.dumps(grupos, ensure_ascii=False, separators=(",", ":")), encoding="utf8")
