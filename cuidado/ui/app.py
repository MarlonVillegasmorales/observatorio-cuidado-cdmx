"""Composición de pantallas; sin ETL ni escrituras a la base operativa."""
from datetime import time
import pandas as pd
import streamlit as st
from cuidado.services.evidencia import cargar_evidencia
from cuidado.services.simulacion import ejecutar_busqueda
from cuidado.services.integraciones import INTEGRACIONES
from cuidado.ui.estilos import aplicar_estilos
from cuidado.ui.territorial import mostrar_visor_territorial, mostrar_comparativo_cuidado, _metricas_principales
from cuidado.ui.mapa_alcaldias import mostrar_comparativo_alcaldias, mostrar_mapa_alcaldias

@st.cache_data(show_spinner='Cargando datos preparados...')
def evidencia():
    return cargar_evidencia()

TAREAS = {
    "Mapa por alcaldía": "Selecciona una alcaldía para consultar sus datos preparados.",
    "Comparar": "Ranking para identificar diferencias territoriales.",
    "Búsqueda demo": "Demostración sintética, sin plazas reales.",
    "Proyecto": "Fuentes, límites y estado académico.",
}

ICONOS_TAREAS = {
    "Mapa por alcaldía": "⌂",
    "Comparar": "≋",
    "Búsqueda demo": "⌕",
    "Proyecto": "i",
    "Información del proyecto": "Fuentes, límites y entregas pendientes.",
}

def _navegar(paso):
    st.session_state["paso_busqueda"] = paso

def _render_busqueda():
    st.markdown('<div class="section-kicker">Exploración guiada · demostración</div>', unsafe_allow_html=True)
    st.header("Búsqueda demostrativa de cuidado")
    st.caption("Explora cómo se comparan filtros con una oferta sintética. No es un servicio de reserva.")
    st.warning(
        "Demostración con datos sintéticos: una recomendación no confirma "
        "una plaza real ni registra personas."
    )
    if "paso_busqueda" not in st.session_state:
        st.session_state["paso_busqueda"] = 1
    paso = st.session_state["paso_busqueda"]
    nombres_pasos = {1: "Servicio", 2: "Horario", 3: "Distancia", 4: "Resultados"}
    st.progress(paso / 4, text=f"Paso {paso} de 4 · {nombres_pasos[paso]}")
    st.caption("Puedes avanzar y regresar; tus respuestas se conservan.")

    tipo = st.selectbox(
        "¿Qué tipo de cuidado buscas?",
        ["infantil", "mayores"],
        format_func=lambda value: "Cuidado infantil" if value == "infantil" else "Cuidado para personas mayores",
        key="busqueda_tipo",
    )
    if paso == 1:
        st.info("Elige el servicio que quieres explorar en esta demostración.")
        if st.button("Continuar a horario", type="primary", key="buscar_paso_1"):
            _navegar(2)
            st.rerun()
        return

    dias = st.multiselect(
        "¿Qué días necesitas?",
        ["lun", "mar"],
        default=["lun", "mar"],
        format_func=lambda value: "Lunes" if value == "lun" else "Martes",
        key="busqueda_dias",
    )
    inicio = st.time_input("Hora de inicio", value=time(9), key="busqueda_inicio")
    fin = st.time_input("Hora de término", value=time(12), key="busqueda_fin")
    if paso == 2:
        st.info("La demostración compara la franja solicitada con la oferta sintética.")
        if st.button("Volver al tipo de cuidado", key="buscar_atras_2"):
            _navegar(1)
            st.rerun()
        if st.button("Continuar a zona", type="primary", key="buscar_paso_2"):
            _navegar(3)
            st.rerun()
        return

    radio = st.slider(
        "Distancia máxima aproximada",
        min_value=1,
        max_value=20,
        value=10,
        format="%d km",
        key="busqueda_radio",
    )
    filtros = (tipo, tuple(dias), inicio, fin, radio)
    if "resultado_busqueda" in st.session_state and filtros != st.session_state.get("filtros_busqueda"):
        st.session_state["busqueda_pendiente"] = True
    if paso == 3:
        st.info("La distancia es geográfica, no un tiempo de viaje.")
        if st.button("Volver al horario", key="buscar_atras_3"):
            _navegar(2)
            st.rerun()
        if st.button("Ver resultados", type="primary", key="buscar_paso_3"):
            st.session_state["busqueda_pendiente"] = False
            st.session_state["filtros_busqueda"] = filtros
            st.session_state["resultado_busqueda"] = ejecutar_busqueda(
                tipo, inicio, fin, dias, radio
            )
            _navegar(4)
            st.rerun()
        return

    if st.session_state.get("busqueda_pendiente"):
        st.warning("Cambiaste un filtro. El resultado anterior está pendiente de actualizar.")
    if st.button("Volver a filtros", key="buscar_atras_4"):
        _navegar(3)
        st.rerun()
    if st.button("Actualizar resultados", type="primary", key="buscar_actualizar"):
        st.session_state["busqueda_pendiente"] = False
        st.session_state["filtros_busqueda"] = filtros
        st.session_state["resultado_busqueda"] = ejecutar_busqueda(
            tipo, inicio, fin, dias, radio
        )
        st.rerun()
    resultado = st.session_state.get("resultado_busqueda")
    if resultado is None:
        st.info("Completa los filtros y ejecuta la búsqueda para ver resultados.")
        return
    for item in resultado:
        estado = "Recomendación sintética" if item["estado"] == "recomendada" else "Sin compatibilidad en esta demostración"
        motivo = {
            "compatible": "Servicio, horario, días, distancia y cupo son compatibles.",
            "sin_servicio_compatible": "No hay un servicio sintético de este tipo.",
            "sin_compatibilidad_horaria": "La franja solicitada no coincide con la oferta.",
            "fuera_de_radio": "La oferta compatible está fuera de la distancia elegida.",
            "sin_cupo": "La oferta compatible no tiene cupo sintético disponible.",
        }[item["motivo"]]
        with st.container(border=True):
            st.subheader(item["centro_id"] or "Sin centro compatible")
            st.markdown(f'<span class="status-pill">{estado}</span>', unsafe_allow_html=True)
            st.write(f"**Motivo:** {motivo}")
            if item["distancia_km"] is not None:
                st.write(f"**Distancia geográfica:** {item['distancia_km']:.3f} km")
            st.caption("Resultado demostrativo; requiere verificación institucional y no confirma una plaza.")


def _render_navegacion(pagina: str) -> str:
    opciones = [f"{ICONOS_TAREAS[tarea]}  {tarea}" for tarea in TAREAS]
    seleccion = st.radio(
        "Secciones del observatorio",
        opciones,
        index=list(TAREAS).index(pagina),
        key="navegacion_principal",
        horizontal=True,
        label_visibility="collapsed",
        format_func=lambda value: value,
    )
    return opciones[[f"{ICONOS_TAREAS[tarea]}  {tarea}" for tarea in TAREAS].index(seleccion)].split("  ", 1)[1]


def _render_proyecto():
    st.markdown('<div class="section-kicker">Sobre este proyecto</div>', unsafe_allow_html=True)
    st.header("Información del proyecto")
    st.caption("Una lectura breve del propósito, alcance y límites del observatorio.")
    bloques = [
        ("Para qué sirve", "Convertir datos de cuidado en evidencia para decisiones y explorar la vinculación con centros comunitarios."),
        ("Qué puedes hacer", "Consultar indicadores de las 16 alcaldías, comparar zonas y recorrer una búsqueda sintética."),
        ("Qué sigue siendo demostrativo", "Las ofertas, solicitudes y resultados de búsqueda son sintéticos; no representan plazas ni centros verificados."),
    ]
    columnas = st.columns(3)
    for columna, (titulo, texto) in zip(columnas, bloques):
        with columna:
            st.markdown(f'<div class="info-card"><h3>{titulo}</h3><p>{texto}</p></div>', unsafe_allow_html=True)
    st.subheader("Fuentes y metodología")
    st.markdown(
        '<div class="section-card"><p>El observatorio conserva las fuentes tabulares y cartográficas del repositorio. '
        "ENUT describe CDMX; la distribución proporcional por alcaldía es exploratoria. "
        "El matching demostrativo compara tipo de servicio, días, horario, radio y cupo.</p></div>",
        unsafe_allow_html=True,
    )
    st.subheader("Limitaciones esenciales")
    st.warning(
        "La infraestructura contabilizada no demuestra cupos disponibles; distancia geográfica no es tiempo de viaje; "
        "la estimación territorial no mide abandono laboral ni causalidad. La aplicación no recoge datos personales."
    )
    st.subheader("Estado académico")
    st.caption("Las entregas internas se muestran como documentación secundaria y no como módulos disponibles.")
    st.dataframe(pd.DataFrame(INTEGRACIONES), hide_index=True, use_container_width=True)
    st.info("Los módulos se incorporarán tras validar sus contratos de entrada y salida. No se muestran ahorros ni recaudaciones inventadas.")

def main():
    st.set_page_config(
        page_title="Observatorio del Cuidado CDMX",
        page_icon="♥",
        layout="wide",
        initial_sidebar_state="collapsed",
    )
    aplicar_estilos()
    st.markdown(
        '<header class="app-header"><div><div class="brand-mark"><span aria-hidden="true">♥</span> Observatorio del cuidado</div>'
        '<div class="territory-label">CDMX <span>· demostración académica</span></div></div></header>',
        unsafe_allow_html=True,
    )
    pagina = _render_navegacion("Mapa por alcaldía")
    st.markdown(f'<p class="task-description">{TAREAS[pagina]}</p>', unsafe_allow_html=True)
    if pagina == "Mapa por alcaldía":
        mostrar_mapa_alcaldias()
    elif pagina == "Comparar":
        mostrar_comparativo_alcaldias()
    elif pagina=="Búsqueda demo":
        _render_busqueda()
    else:
        _render_proyecto()
