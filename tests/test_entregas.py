from cuidado.pipelines.entregas import (
    cargar_conapo,
    cargar_empresas,
    cargar_movilidad,
    validar_entregas,
)


def test_entregas_procesadas_conservan_cobertura():
    resumen = validar_entregas()
    assert resumen["conapo_filas"] == 320
    assert resumen["conapo_alcaldias"] == 16
    assert resumen["movilidad_filas"] == 22532
    assert resumen["empresas_filas"] == 50
    assert resumen["empresas_alcaldias"] == 16


def test_empresas_preservan_cp_y_marca_sintetica():
    data = cargar_empresas()
    assert data["d_codigo"].str.fullmatch(r"\d{5}").all()
    assert data["es_simulada"].all()
    assert set(data["tipo_dato"]) == {"sintetico"}


def test_movilidad_no_confunde_relacion_con_tiempo():
    data = cargar_movilidad()
    assert data["representa_tiempo_viaje"].eq(False).all()
    assert not data.duplicated(["route_id", "stop_id"]).any()


def test_conapo_marca_proyecciones_y_periodos():
    data = cargar_conapo()
    assert data["es_proyeccion"].all()
    assert data["ANO"].between(2021, 2030).all()
