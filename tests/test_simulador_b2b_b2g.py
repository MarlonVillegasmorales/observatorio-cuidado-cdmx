import math

import pytest

from cuidado.services.simulador_b2b_b2g import (
    cargar_escenarios,
    ejecutar_escenarios,
    simular_b2b,
    simular_b2g,
)


def test_carga_y_ejecucion_de_30_escenarios():
    data = cargar_escenarios()
    results = ejecutar_escenarios()
    assert len(data) == 30
    assert len(results) == 30
    assert results["b2b_beneficio_neto"].isna().all()
    assert (results["b2g_total_impuestos"] >= 0).all()


def test_simulador_rechaza_valores_invalidos():
    row = cargar_escenarios().iloc[0].to_dict()
    row["reduccion_rotacion_pct"] = 101
    with pytest.raises(ValueError, match="reduccion_rotacion_pct"):
        simular_b2b(row)

    row = cargar_escenarios().iloc[0].to_dict()
    row["tasa_isn_cdmx"] = math.inf
    with pytest.raises(ValueError, match="finito"):
        simular_b2g(row)


def test_b2g_separa_impuesto_y_aportaciones():
    row = cargar_escenarios().iloc[0].to_dict()
    result = simular_b2g(row)
    assert result["total_impuestos"] == result["isn_impuesto"]
    assert result["total_flujos_publicos"] == pytest.approx(
        result["total_impuestos"] + result["total_aportaciones"]
    )
