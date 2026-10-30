from pathlib import Path
from streamlit.testing.v1 import AppTest

ROOT=Path(__file__).resolve().parents[1]

def test_task_navigation_and_project_page():
    app=AppTest.from_file(str(ROOT/'app_dashboard.py'),default_timeout=90).run()
    assert not app.exception
    assert app.session_state["seccion_activa"] == "Inicio"
    assert app.button(key="inicio_mapa").label == "Explorar mapa"
    for key in ["inicio_mapa", "inicio_comparar", "inicio_busqueda"]:
        app.button(key=key).click().run()
        assert not app.exception
        assert app.session_state["seccion_activa"] in {"Mapa", "Comparar", "Búsqueda demo"}
        app.session_state["seccion_activa"] = "Inicio"
        app.run()
    app.button(key="menu_toggle").click().run()
    app.button(key="menu_proyecto").click().run()
    assert app.session_state["seccion_activa"] == "Proyecto"
    assert any("Información del proyecto" in element.value for element in app.header)

def test_search_keeps_form_values_and_marks_stale_results():
    app=AppTest.from_file(str(ROOT/'app_dashboard.py'),default_timeout=90).run()
    app.session_state["seccion_activa"] = "Búsqueda demo"
    app.run()
    app.button(key='buscar_paso_1').click().run()
    app.button(key='buscar_paso_2').click().run()
    app.button(key='buscar_paso_3').click().run()
    assert not app.exception
    assert app.session_state['paso_busqueda'] == 4
    app.selectbox(key='busqueda_tipo').set_value('mayores').run()
    assert app.session_state['busqueda_tipo'] == 'mayores'
    assert any('pendiente de actualizar' in warning.value for warning in app.warning)
    app.button(key='buscar_actualizar').click().run()
    assert not app.exception
    assert any('No hay un servicio sintético' in text.value for text in app.markdown)
