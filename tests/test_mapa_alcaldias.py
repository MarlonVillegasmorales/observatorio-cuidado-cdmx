import json
from pathlib import Path

import geopandas as gpd
import pandas as pd
import pytest

from cuidado.pipelines.mapa_alcaldias import (
    DEFAULT_CENSO,
    DEFAULT_OBSERVATORIO,
    DEFAULT_SHAPEFILE,
    EXPECTED_KEYS,
    preparar_mapa_alcaldias,
)
from cuidado.services.mapa_alcaldias import (
    cargar_mapa_alcaldias,
    indicadores_de_alcaldia,
    indicadores_publicos,
)
from cuidado.ui.mapa_alcaldias import _fila_60_mas


@pytest.fixture(scope="module")
def mapa_preparado(tmp_path_factory: pytest.TempPathFactory) -> Path:
    return preparar_mapa_alcaldias(
        output_dir=tmp_path_factory.mktemp("mapa_alcaldias"),
        ruta_censo=DEFAULT_CENSO,
        ruta_observatorio=DEFAULT_OBSERVATORIO,
        ruta_shapefile=DEFAULT_SHAPEFILE,
    )


def test_tiene_las_16_claves_y_geometrias_validas(mapa_preparado: Path) -> None:
    geometria = gpd.read_file(mapa_preparado / "alcaldias.geojson")
    assert set(geometria["clave"]) == EXPECTED_KEYS
    assert geometria["clave"].is_unique
    assert geometria.geometry.is_valid.all()
    assert not geometria.geometry.is_empty.any()
    assert str(geometria.crs) == "EPSG:4326"


def test_uniones_indicadores_sin_perdidas_ni_duplicados(
    mapa_preparado: Path,
) -> None:
    geometria = gpd.read_file(mapa_preparado / "alcaldias.geojson")
    indicadores = pd.read_parquet(mapa_preparado / "indicadores_alcaldia.parquet")
    assert set(indicadores["clave_alcaldia"]) == EXPECTED_KEYS
    assert not indicadores.duplicated(
        ["clave_alcaldia", "id_indicador", "periodo"]
    ).any()
    assert indicadores["valor"].notna().all()
    assert set(indicadores["clave_alcaldia"]) == set(geometria["clave"])


def test_rangos_y_conciliacion_de_edad(mapa_preparado: Path) -> None:
    indicadores = pd.read_parquet(mapa_preparado / "indicadores_alcaldia.parquet")
    porcentaje = indicadores.loc[
        indicadores["id_indicador"] == "discapacidad_porcentaje", "valor"
    ]
    assert porcentaje.between(0, 100).all()

    calidad = json.loads((mapa_preparado / "calidad_mapa.json").read_text())
    assert calidad["coherencia_grupos_edad"]["diferencia_maxima"] == 0
    assert calidad["divisiones_por_cero"] == 0


def test_estimaciones_no_verificadas_no_forman_parte_del_conjunto(
    mapa_preparado: Path,
) -> None:
    indicadores = pd.read_parquet(mapa_preparado / "indicadores_alcaldia.parquet")
    excluidos = {
        "cobertura_caci_0_2_pct",
        "poblacion_total_infantes_0_2",
        "personas_afectadas",
        "estimacion_cuidadores_sin_trabajo_mercado",
        "guarderias_por_1000_habitantes",
    }
    assert excluidos.isdisjoint(set(indicadores["id_indicador"]))


def test_consulta_de_cada_alcaldia_y_claves_invalidas() -> None:
    geometria, indicadores, catalogo, _ = cargar_mapa_alcaldias.__wrapped__()
    claves = set(geometria["clave"].astype(str))
    assert len(claves) == 16
    for clave in claves:
        filas = indicadores_de_alcaldia(indicadores, clave)
        assert not filas.empty
        assert set(filas["clave_alcaldia"]) == {clave}
        assert _fila_60_mas(indicadores, clave)["valor"] > 0
    assert indicadores_de_alcaldia(indicadores, "").empty
    assert indicadores_de_alcaldia(indicadores, "clave-inexistente").empty


def test_poblacion_oficial_y_exclusiones_publicas() -> None:
    _, indicadores, catalogo, _ = cargar_mapa_alcaldias.__wrapped__()
    publicos = indicadores_publicos(indicadores, catalogo)
    iztapalapa = publicos.loc[
        (publicos["clave_alcaldia"] == "09 007")
        & publicos["id_indicador"].isin(["poblacion_total", "pob_0_4"])
    ].set_index("id_indicador")["valor"]
    assert iztapalapa.to_dict() == {
        "poblacion_total": 3670972.0,
        "pob_0_4": 206296.0,
    }
    assert "guarderias_conteo" not in set(publicos["id_indicador"])
    assert "estimacion_cuidadores_sin_trabajo_mercado" not in set(publicos["id_indicador"])
