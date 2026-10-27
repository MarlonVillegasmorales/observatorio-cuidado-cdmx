"""Composición de pantallas; sin ETL ni escrituras a la base operativa."""
from datetime import time
import pandas as pd
import streamlit as st
from cuidado.services.evidencia import cargar_evidencia
from cuidado.services.simulacion import ejecutar_busqueda
from cuidado.services.integraciones import INTEGRACIONES
from cuidado.ui.estilos import aplicar_estilos
from cuidado.ui.territorial import mostrar_visor_territorial, mostrar_comparativo_cuidado, _metricas_principales

@st.cache_data(show_spinner='Cargando datos preparados...')
def evidencia():
    return cargar_evidencia()

TAREAS = {
    "Conocer mi zona": "Mapa e indicadores de cuidado por alcaldía.",
    "Comparar zonas": "Ranking para identificar diferencias territoriales.",
    "Probar una búsqueda de cuidado": "Demostración sintética, sin plazas reales.",
    "Información del proyecto": "Fuentes, límites y entregas pendientes.",
}

def _navegar(paso):
    st.session_state["paso_busqueda"] = paso

def _render_busqueda():
    st.header("Probar una búsqueda de cuidado")
    st.warning(
        "Esta búsqueda usa datos completamente sintéticos. Una recomendación "
        "no confirma una plaza real ni registra personas."
    )
    if "paso_busqueda" not in st.session_state:
        st.session_state["paso_busqueda"] = 1
    paso = st.session_state["paso_busqueda"]
    st.progress(paso / 4, text=f"Paso {paso} de 4")
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
            st.subheader(estado)
            st.write(f"**Motivo:** {motivo}")
            if item["distancia_km"] is not None:
                st.write(f"**Distancia geográfica:** {item['distancia_km']:.3f} km")
            st.caption("Resultado demostrativo; requiere verificación institucional y no confirma una plaza.")

def main():
    st.set_page_config(page_title='Observatorio del Cuidado CDMX',layout='wide')
    aplicar_estilos()
    st.markdown('<div class="brand-mark"><span aria-hidden="true">♥</span> Observatorio del cuidado</div>', unsafe_allow_html=True)
    st.title('Economía del cuidado en CDMX')
    st.caption('Segundo avance · explora datos territoriales y una búsqueda sintética')
    pagina = st.sidebar.radio(
        "¿Qué quieres hacer?",
        list(TAREAS),
    )
    st.sidebar.caption(TAREAS[pagina])
    if pagina in ['Conocer mi zona','Comparar zonas']:
        try:
            data=evidencia()
        except (FileNotFoundError,ValueError) as error:
            st.error(str(error)); return
        st.info('Los indicadores combinan años y poblaciones de referencia distintos. La estimación territorial de cuidado sin trabajo de mercado no mide abandono laboral ni causalidad.')
        _metricas_principales(data)
        if pagina=='Conocer mi zona': mostrar_visor_territorial(data)
        else: mostrar_comparativo_cuidado(data)
    elif pagina=='Probar una búsqueda de cuidado':
        _render_busqueda()
    else:
        st.header('Información del proyecto')
        st.subheader('Entregas pendientes del equipo')
        st.dataframe(pd.DataFrame(INTEGRACIONES),hide_index=True,use_container_width=True)
        st.info('Los módulos se incorporarán tras validar sus contratos de entrada y salida. No se muestran ahorros ni recaudaciones inventadas.')
        with st.expander("Fuentes, definiciones y límites", expanded=True):
            st.markdown('''El observatorio conserva las fuentes tabulares y cartográficas del repositorio. ENUT describe CDMX; la distribución proporcional por alcaldía es exploratoria.

El dato de horas de mujeres cuidadoras procede del resumen ENUT, separado de los indicadores macroeconómicos. El conteo de infraestructura no demuestra cupos disponibles.

El matching demostrativo exige tipo de servicio, días, horario, radio y cupo. No es un modelo entrenado para predecir inserción laboral y no sustituye verificación institucional.

La aplicación pública no recoge datos personales. Antes de habilitar operación real faltan autenticación, autorización por rol, protocolo de privacidad, verificación de centros, migración de registros y seguimiento del piloto.''')
