from pathlib import Path
from streamlit.testing.v1 import AppTest

ROOT = Path(__file__).resolve().parents[1]


def test_task_navigation_and_project_page():
    app = AppTest.from_file(str(ROOT / "app_dashboard.py"), default_timeout=90).run()
    assert not app.exception
    assert app.session_state["seccion_activa"] == "Inicio"
    assert app.button(key="inicio_mapa").label == "Explorar mapa"
    for key, expected in [
        ("inicio_mapa", "Mapa"),
        ("inicio_comparar", "Comparar"),
        ("inicio_propuesta_publica", "Propuesta pública"),
        ("inicio_alianza", "Alianza público privada"),
    ]:
        app.button(key=key).click().run()
        assert not app.exception
        assert app.session_state["seccion_activa"] == expected
        app.session_state["seccion_activa"] = "Inicio"
        app.run()
    app.button(key="menu_toggle").click().run()
    app.button(key="menu_proyecto").click().run()
    assert app.session_state["seccion_activa"] == "Proyecto"
    assert any("Información del proyecto" in element.value for element in app.header)


def test_public_proposal_displays_territorial_evidence_and_cost():
    app = AppTest.from_file(str(ROOT / "app_dashboard.py"), default_timeout=90).run()
    app.session_state["seccion_activa"] = "Propuesta pública"
    app.run()
    assert not app.exception
    assert any("Propuesta pública de cuidado infantil" in element.value for element in app.header)
    assert any(metric.value == "5.5%" for metric in app.metric)
    assert any("Costo anual de operación por centro" in element.value for element in app.subheader)
    assert any("14.62 millones por centro" in element.value for element in app.caption)


def test_public_private_partnership_shows_scenario_and_savings_limit():
    app = AppTest.from_file(str(ROOT / "app_dashboard.py"), default_timeout=90).run()
    app.session_state["seccion_activa"] = "Alianza público privada"
    app.run()
    assert not app.exception
    assert any("Alianza público privada" in element.value for element in app.header)
    metric_values = [str(metric.value) for metric in app.metric]
    assert any("91,402" in value for value in metric_values)
    visible_text = " ".join(
        str(element.value)
        for collection in (app.markdown, app.caption, app.subheader, app.warning, app.info)
        for element in collection
    )
    assert "Ahorro observado por menor rotación" in visible_text
    assert "no retorno medido en Iztapalapa" in visible_text


def test_comparison_has_distinct_selections_and_composition():
    app = AppTest.from_file(str(ROOT / "app_dashboard.py"), default_timeout=90).run()
    app.session_state["seccion_activa"] = "Comparar"
    app.run()
    assert not app.exception
    assert any("Compara dos alcaldías" in element.value for element in app.header)
    assert app.session_state["comparativo_alcaldia_a"] != app.session_state["comparativo_alcaldia_b"]
    assert any("Personas de 0 a 4 años" in element.value for element in app.subheader)
    assert any("Personas de 60 años o más" in element.value for element in app.subheader)
