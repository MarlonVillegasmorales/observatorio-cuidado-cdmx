"""Composición de pantallas; sin ETL ni escrituras a la base operativa."""
import json
from pathlib import Path
from datetime import time
import pandas as pd
import streamlit as st
from cuidado.services.simulacion import ejecutar_busqueda
from cuidado.services.integraciones import INTEGRACIONES
from cuidado.services.simulador_b2b_b2g import (
    cargar_escenarios,
    simular_b2b,
    simular_b2g,
)
from cuidado.ui.estilos import aplicar_estilos

@st.cache_data(show_spinner='Cargando datos preparados...')
def evidencia():
    from cuidado.services.evidencia import cargar_evidencia

    return cargar_evidencia()

TAREAS = {
    "Inicio": "Una entrada breve para elegir qué explorar.",
    "Mapa": "Selecciona una alcaldía para consultar sus datos preparados.",
    "Comparar": "Ranking para identificar diferencias territoriales.",
    "Propuesta pública": "Brecha territorial y costos de operación para Iztapalapa.",
    "Alianza público privada": "Reparto de costos, aportes empresariales y condiciones de viabilidad.",
    "Proyecto": "Fuentes, límites y estado académico.",
    "Privacidad": "Información del directorio, demostraciones y piloto.",
}

ICONOS_TAREAS = {
    "Privacidad": "",
    "Inicio": "⌂",
    "Mapa": "⌖",
    "Comparar": "≋",
    "Propuesta pública": "▦",
    "Alianza público privada": "⇄",
    "Proyecto": "i",
}
CLAVES_NAVEGACION = {
    "Privacidad": "privacidad",
    "Inicio": "inicio",
    "Mapa": "mapa",
    "Comparar": "comparar",
    "Propuesta pública": "propuesta_publica",
    "Alianza público privada": "alianza",
    "Proyecto": "proyecto",
}

def _navegar(paso):
    st.session_state["paso_busqueda"] = paso

def _render_busqueda():
    st.markdown('<div class="section-kicker">Exploración guiada · demostración</div>', unsafe_allow_html=True)
    st.header("Búsqueda demostrativa de cuidado")
    st.caption("Prueba días y horarios de ejemplo. El resultado se calcula con oferta simulada y no genera una solicitud o reserva.")
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


def _ir_a(seccion: str) -> None:
    if seccion not in TAREAS:
        raise ValueError(f"Sección de navegación desconocida: {seccion}")
    st.session_state["seccion_activa"] = seccion


def _render_inicio() -> None:
    st.markdown('<div class="section-kicker">Observatorio del cuidado</div>', unsafe_allow_html=True)
    st.header("Economía del cuidado en CDMX")
    st.write("Explora los centros de cuidado infantil documentados en las 16 alcaldías. Consulta sus horarios publicados y compara la información disponible.")
    st.image(str(Path(__file__).resolve().parents[2] / "cliente_flutter/assets/portada.webp"), width=640)
    st.subheader("¿Qué quieres explorar?")
    accesos = [
        ("Explorar mapa", "Mapa", "mapa", "Localiza centros y consulta sus horarios."),
        ("Comparar alcaldías", "Comparar", "comparar", "Compara sedes con horario publicado y grupos de edad."),
        ("Propuesta pública", "Propuesta pública", "propuesta_publica", "Consulta cobertura, brecha territorial y costo operativo en Iztapalapa."),
        ("Alianza público privada", "Alianza público privada", "alianza", "Explora aportes, escenarios de consorcio y el umbral de comparación laboral."),
    ]
    accesos.append(("Cómo usamos los datos", "Privacidad", "privacidad", "Consulta la privacidad del mapa y el aviso del piloto."))
    columnas = st.columns(len(accesos))
    for columna, (etiqueta, destino, clave, descripcion) in zip(columnas, accesos):
        with columna:
            st.markdown(f'<div class="action-card"><h3>{etiqueta}</h3><p>{descripcion}</p></div>', unsafe_allow_html=True)
            if st.button(etiqueta, type="primary", key=f"inicio_{clave}"):
                _ir_a(destino)
                st.rerun()


def _render_navegacion(pagina: str) -> None:
    if pagina not in TAREAS:
        pagina = "Inicio"
        _ir_a(pagina)
    opciones = list(TAREAS)
    with st.container(key="nav-desktop"):
        st.caption("Navegación principal")
        columnas = st.columns(len(opciones))
        for columna, opcion in zip(columnas, opciones):
            with columna:
                if st.button(
                    f"{ICONOS_TAREAS[opcion]}  {opcion}",
                    key=f"nav_{CLAVES_NAVEGACION[opcion]}",
                    type="primary" if opcion == pagina else "secondary",
                    use_container_width=True,
                ):
                    _ir_a(opcion)
                    st.rerun()
    with st.container(key="nav-mobile"):
        st.caption(f"Sección actual: {pagina}")
        if "menu_abierto" not in st.session_state:
            st.session_state["menu_abierto"] = False
        if st.button("Menú", key="menu_toggle", use_container_width=True):
            st.session_state["menu_abierto"] = not st.session_state["menu_abierto"]
            st.rerun()
        if st.session_state["menu_abierto"]:
            with st.container(key="menu-items"):
                st.markdown("**Navegación principal**")
                for opcion in opciones:
                    if st.button(
                        f"{ICONOS_TAREAS[opcion]}  {opcion}",
                        key=f"menu_{CLAVES_NAVEGACION[opcion]}",
                        type="primary" if opcion == pagina else "secondary",
                        use_container_width=True,
                    ):
                        _ir_a(opcion)
                        st.session_state["menu_abierto"] = False
                        st.rerun()


def _render_propuesta_publica() -> None:
    st.markdown('<div class="section-kicker">Piloto territorial · Iztapalapa</div>', unsafe_allow_html=True)
    st.header("Propuesta pública de cuidado infantil")
    st.info(
        "La cobertura corresponde a CACI públicos para niñas y niños de 0 a 2 años en 2023. "
        "La expansión propuesta por Evalúa considera población de 0 a 5 años."
    )

    metricas = [
        ("Cobertura pública", "5.5%", "Iztapalapa · 0–2 años · 2023"),
        ("Matrícula", "3,164", "niñas y niños · 2023"),
        ("Población de referencia", "57,907", "niñas y niños · 0–2 años"),
        ("CACI públicos", "48", "centros reportados · 2023"),
    ]
    cols = st.columns(4)
    for col, (label, value, note) in zip(cols, metricas):
        with col:
            with st.container(border=True):
                st.metric(label, value)
                st.caption(note)

    st.subheader("Brecha de cobertura")
    cobertura = pd.DataFrame(
        {"Cobertura (%)": [2.9, 5.5, 10.7]},
        index=["Milpa Alta", "Iztapalapa", "Ciudad de México"],
    )
    st.bar_chart(cobertura, y="Cobertura (%)", use_container_width=True)
    st.caption(
        "Iztapalapa está por debajo del promedio de CDMX, pero no es la alcaldía con menor cobertura. "
        "Milpa Alta registró 2.9%. Fuente: Evalúa CDMX, 2023."
    )

    st.subheader("Distancia media al CACI más cercano")
    distancias = pd.DataFrame(
        {"Distancia (m)": [2319, 1260, 906, 757, 2000]},
        index=["Gobierno CDMX", "Alcaldía", "Privados", "Comunitarios", "CACI nacionales"],
    )
    st.bar_chart(distancias, y="Distancia (m)", use_container_width=True)
    st.caption(
        "Promedios de 2020 para colonias de zonas ampliadas de concentración infantil. "
        "No representan recorridos por domicilio ni tiempos actuales de viaje. Fuente: Evalúa CDMX."
    )

    st.subheader("Expansión territorial propuesta")
    expansion = [
        ("41", "espacios para nuevos centros", "Propuesta de planeación; no instalaciones construidas."),
        ("67,146", "niñas y niños de 0 a 5 años", "Población potencial, no usuarios confirmados."),
        ("117", "plazas por centro tipo", "Referencia de costeo; requiere validación por inmueble."),
    ]
    cols = st.columns(3)
    for col, (value, label, note) in zip(cols, expansion):
        with col:
            with st.container(border=True):
                st.metric(label, value)
                st.caption(note)

    st.subheader("Costo anual de operación por centro")
    costos = pd.DataFrame(
        {"Millones de MXN": [13.72, 14.62]},
        index=["Referencia a precios de 2024", "Actualización indicativa a oct. 2026"],
    )
    st.bar_chart(costos, y="Millones de MXN", use_container_width=True)
    st.caption(
        "Evalúa estimó $562.58 millones anuales para 41 centros propuestos, sin construcción. "
        "El promedio aritmético es $13.72 millones por centro. La actualización a octubre de 2026 "
        "es $14.62 millones por centro/año y $124,994 por plaza/año a ocupación plena. "
        "Usa el INPC general; no es cotización, presupuesto aprobado ni costo total con obra."
    )

    with st.expander("Fuentes y límites"):
        st.markdown(
            "- [Evalúa CDMX · evaluación del sistema de cuidados](https://www.evalua.cdmx.gob.mx/storage/app/media/2024/se/ee/cuidados/evaluacion-cuidados-vf.pdf)\\n"
            "- [Evalúa CDMX · opinión técnica de presupuesto 2024–2025](https://www.evalua.cdmx.gob.mx/storage/app/media/2024/se/opinion-de-presupuesto-para-2024-2025.pdf)\\n"
            "- [INEGI · INPC octubre de 2026](https://www.inegi.org.mx/contenidos/saladeprensa/boletines/2026/inpc/inpc_2q2026_11.pdf)\\n"
            "- [INEGI · INPC diciembre de 2024](https://www.inegi.org.mx/contenidos/saladeprensa/boletines/2025/inpc/inpc_2q2025_01.pdf)"
        )
        st.warning(
            "Evalúa no publica el listado de los 41 sitios con nombre y coordenadas. "
            "Siguen pendientes el inmueble, costo de obra, permisos, capacidad autorizada y presupuesto vigente."
        )


def _render_alianza_publico_privada() -> None:
    import matplotlib.pyplot as plt

    costo = 14_624_331.31
    costo_contratacion = 33_934
    st.markdown('<div class="section-kicker">Modelo de coparticipación · Iztapalapa</div>', unsafe_allow_html=True)
    st.header("Alianza público privada")
    st.info(
        "Este modelo distribuye el costo operativo estimado de un centro tipo. "
        "Es un escenario de diseño: no representa un convenio, presupuesto aprobado ni ahorro observado."
    )

    col_reparto, col_empresas = st.columns(2)
    with col_reparto:
        porcentaje_privado = st.select_slider(
            "Porcentaje del costo aportado por empresas",
            options=[25, 50, 75],
            value=25,
            format_func=lambda value: f"{value}% empresas / {100 - value}% público",
            key="alianza_porcentaje_privado",
        )
    with col_empresas:
        numero_empresas = st.select_slider(
            "Empresas participantes",
            options=[10, 20, 40],
            value=40,
            format_func=lambda value: f"{value} empresas",
            key="alianza_numero_empresas",
        )

    aporte_privado = costo * porcentaje_privado / 100
    aporte_publico = costo - aporte_privado
    por_empresa = aporte_privado / numero_empresas
    equivalentes_contratacion = por_empresa / costo_contratacion

    st.subheader("Reparto anual del costo")
    fig, ax = plt.subplots(figsize=(8.2, 1.35))
    ax.barh(["Operación de un centro tipo"], [aporte_publico / 1_000_000], color="#4C1D95", label="Gobierno")
    ax.barh(
        ["Operación de un centro tipo"],
        [aporte_privado / 1_000_000],
        left=[aporte_publico / 1_000_000],
        color="#A78BFA",
        label="Empresas",
    )
    ax.set_xlim(0, costo / 1_000_000 * 1.04)
    ax.set_xlabel("Millones de MXN al año")
    ax.legend(loc="lower center", bbox_to_anchor=(0.5, 1.03), ncol=2, frameon=False)
    ax.spines[["top", "right", "left"]].set_visible(False)
    ax.tick_params(axis="y", length=0)
    ax.grid(axis="x", alpha=0.18)
    ax.set_axisbelow(True)
    fig.tight_layout()
    st.pyplot(fig, use_container_width=True)
    plt.close(fig)

    c1, c2, c3 = st.columns(3)
    with c1:
        st.metric("Aportación pública", f"${aporte_publico:,.0f}", f"{100 - porcentaje_privado}% del costo")
    with c2:
        st.metric("Aportación empresarial conjunta", f"${aporte_privado:,.0f}", f"{porcentaje_privado}% del costo")
    with c3:
        st.metric("Aporte anual por empresa", f"${por_empresa:,.0f}", f"si participan {numero_empresas}")

    with st.container(border=True):
        st.subheader("Umbral para comparar con contratación")
        st.metric(
            "Contrataciones equivalentes por empresa",
            f"{equivalentes_contratacion:.1f}",
            f"Aporte anual ÷ ${costo_contratacion:,.0f}",
        )
        st.caption(
            "Grupo BMV reportó un promedio de  $33,934 por contratación a partir de 127 vacantes cubiertas "
            "(91 externas). Es una referencia parcial, no el costo completo de reemplazo. "
            "La equivalencia no indica cuántas salidas ocurren o se evitarían."
        )

    st.subheader("Aporte por empresa según tamaño del consorcio")
    cantidades = [10, 20, 40]
    aportes = [aporte_privado / n for n in cantidades]
    fig, ax = plt.subplots(figsize=(7.5, 3.2))
    barras = ax.bar([str(n) for n in cantidades], aportes, color=["#4C1D95", "#8B5CF6", "#A78BFA"])
    ax.set_xticks(range(len(cantidades)), [f"{n} empresas" for n in cantidades])
    ax.set_ylabel("MXN por empresa / año")
    ax.set_title(f"Aporte privado total: ${aporte_privado:,.0f} por año")
    ax.spines[["top", "right"]].set_visible(False)
    ax.grid(axis="y", alpha=0.18)
    ax.set_axisbelow(True)
    for barra, valor in zip(barras, aportes):
        ax.text(barra.get_x() + barra.get_width() / 2, valor, f"${valor:,.0f}", ha="center", va="bottom", fontsize=9)
    fig.tight_layout()
    st.pyplot(fig, use_container_width=True)
    plt.close(fig)

    st.subheader("Sectores candidatos para orientar el piloto")
    st.caption("La participación femenina es de CDMX (2023); la rotación es nacional (Censo Económico 2019), total y sin desglose por sexo.")
    sectores = pd.DataFrame({
        "Comercio minorista": [16.5, 25.1, 30.6, 28.8],
        "Hoteles y restaurantes": [13.1, 27.2, 39.4, 38.3],
    }, index=["Hasta 10 personas", "11–50", "51–250", "251 o más"])
    fig, ax = plt.subplots(figsize=(8, 3.4))
    sectores.plot(kind="bar", ax=ax, color=["#4C1D95", "#A78BFA"], width=0.78)
    ax.set_ylabel("Rotación total (%)")
    ax.set_xlabel("Personas ocupadas por establecimiento · México · 2019")
    ax.legend(frameon=False)
    ax.spines[["top", "right"]].set_visible(False)
    ax.grid(axis="y", alpha=0.18)
    ax.set_axisbelow(True)
    fig.tight_layout()
    st.pyplot(fig, use_container_width=True)
    plt.close(fig)
    st.caption("En CDMX, las mujeres fueron 47.0% del personal de comercio minorista y 48.2% en hoteles y restaurantes en 2023. Estos indicadores orientan sectores; no prueban rotación actual de trabajadoras en Iztapalapa ni efecto del cuidado.")

    with st.container(border=True):
        st.subheader("Ahorro observado por menor rotación")
        st.write("No disponible en las fuentes públicas revisadas. La app no convierte los porcentajes hipotéticos anteriores en ahorro.")
        st.caption("Para demostrar ahorro se necesitan costos empresariales de reemplazo y medir permanencia antes y después del apoyo.")

    st.subheader("Cómo se estructura el mecanismo")
    st.write(
        "En CECI en Empresa, la empresa aporta terreno, construcción y equipamiento; el IMSS cubre al patrón "
        "una cuota mensual por niña o niño inscrito conforme al convenio, y participa en regulación y capacitación. "
        "La cuota se determina en el convenio: aquí no se fija una tarifa universal."
    )
    st.warning(
        "El anuncio de recuperación en cinco años supone ocupación del 100% y es una proyección, no un retorno "
        "medido en Iztapalapa. El costo usado en esta pantalla es operación indicativa y excluye construcción, "
        "remodelación, administración empresarial y aportaciones contractuales del IMSS."
    )

    with st.expander("Fuentes y límites"):
        st.markdown(
            "- [Evalúa CDMX · costo y propuesta territorial](https://www.evalua.cdmx.gob.mx/storage/app/media/2024/se/ee/cuidados/evaluacion-cuidados-vf.pdf)\\n"
            "- [IMSS · acuerdo de CECI en Empresa, 2026](https://sidof.segob.gob.mx/notas/docFuente/5784757)\\n"
            "- [Secretaría de Economía · modelo CECI en Empresa](https://www.gob.mx/se/prensa/economia-el-bid-y-la-cepal-impulsan-la-construccion-de-infraestructura-de-cuidados-en-empresas-y-parques-industriales?idiom=es-MX)\\n"
            "- [Grupo BMV · Informe Anual Integrado 2025](https://www.bmv.com.mx/docs-pub/informeAnual/Informe%20Anual%20Integrado%20Grupo%20BMV_2025.pdf)\\n"
            "- [INEGI · Censos Económicos 2024, CDMX](https://www.inegi.org.mx/contenidos/saladeprensa/boletines/2025/ce/CE_2024_Def_CdMx.pdf)\\n"
            "- [Data México · comercio minorista](https://www.economia.gob.mx/datamexico/es/profile/industry/retail-trade) · [hoteles y restaurantes](https://www.economia.gob.mx/datamexico/es/profile/industry/accommodation-and-food-services)\\n"
            "- [IFC · caso Grupo Coppel](https://www.ifc.org/es/pressroom/2025/ifc-and-grupo-coppel-study)"
        )


def _render_simuladores() -> None:
    st.markdown('<div class="section-kicker">Escenarios sintéticos</div>', unsafe_allow_html=True)
    st.header("Simuladores B2B y B2G")
    st.info(
        "Usa cifras hipotéticas o agregadas de la empresa. Los resultados demostrativos no estiman impacto observado ni beneficio neto "
        "cuando falta el costo de intervención."
    )
    try:
        escenarios = cargar_escenarios()
    except (FileNotFoundError, ValueError) as exc:
        st.error(f"No se pudieron cargar los escenarios: {exc}")
        return

    ids = escenarios["escenario_id"].tolist()
    seleccionado = st.selectbox("Escenario", ids, key="simulador_escenario")
    row = escenarios.loc[escenarios["escenario_id"] == seleccionado].iloc[0].to_dict()

    col1, col2 = st.columns(2)
    with col1:
        row["numero_empleadas"] = st.number_input(
            "Número de empleadas", min_value=1.0, value=float(row["numero_empleadas"]), step=1.0
        )
        row["salario_promedio"] = st.number_input(
            "Salario promedio mensual", min_value=0.01, value=float(row["salario_promedio"]), step=100.0
        )
        row["bajas_anuales"] = st.number_input(
            "Bajas anuales", min_value=0.0, value=float(row["bajas_anuales"]), step=1.0
        )
        row["reduccion_rotacion_pct"] = st.number_input(
            "Reducción de rotación (%)", min_value=0.0, max_value=100.0,
            value=float(row["reduccion_rotacion_pct"]), step=1.0
        )
    with col2:
        row["dias_cotizados"] = st.number_input(
            "Días cotizados", min_value=1.0, max_value=366.0,
            value=float(row["dias_cotizados"]), step=1.0
        )
        row["factor_integracion_sbc"] = st.number_input(
            "Factor de integración SBC", min_value=0.01,
            value=float(row["factor_integracion_sbc"]), step=0.01
        )
        row["tasa_imss_patronal"] = st.number_input(
            "Tasa IMSS patronal", min_value=0.0, max_value=1.0,
            value=float(row["tasa_imss_patronal"]), step=0.01
        )
        row["tasa_isn_cdmx"] = st.number_input(
            "Tasa ISN CDMX", min_value=0.0, max_value=1.0,
            value=float(row["tasa_isn_cdmx"]), step=0.01
        )
        row["tasa_infonavit"] = st.number_input(
            "Tasa INFONAVIT", min_value=0.0, max_value=1.0,
            value=float(row["tasa_infonavit"]), step=0.01
        )

    if st.button("Calcular escenario", type="primary", key="calcular_simulador"):
        try:
            b2b = simular_b2b(row)
            b2g = simular_b2g(row)
        except ValueError as exc:
            st.error(str(exc))
            return
        st.subheader("Ahorro y beneficio B2B")
        st.metric("Ahorro bruto", f"${b2b['ahorro_bruto']:,.2f} MXN")
        st.metric(
            "Beneficio neto",
            "No calculable"
            if b2b["beneficio_neto"] is None
            else f"${b2b['beneficio_neto']:,.2f} MXN",
        )
        st.subheader("Flujos públicos B2G")
        st.metric("ISN — impuesto", f"${b2g['isn_impuesto']:,.2f} MXN")
        st.metric("IMSS — aportación", f"${b2g['imss_patronal']:,.2f} MXN")
        st.metric("INFONAVIT — aportación", f"${b2g['infonavit_aportacion']:,.2f} MXN")


def _render_proyecto():
    st.markdown('<div class="section-kicker">Sobre este proyecto</div>', unsafe_allow_html=True)
    st.header("Información del proyecto")
    st.caption("Una lectura breve del propósito, alcance y límites del observatorio.")
    bloques = [
        ("Para qué sirve", "Convertir datos de cuidado en evidencia para decisiones y explorar la vinculación con centros comunitarios."),
        ("Qué puedes hacer", "Consultar indicadores de las 16 alcaldías, comparar zonas, ejecutar matching sintético y calcular escenarios B2B/B2G."),
        ("Qué sigue siendo demostrativo", "Las ofertas, solicitudes y escenarios son sintéticos; no representan plazas ni impacto observado."),
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
        "la estimación territorial no mide abandono laboral ni causalidad. El mapa se consulta sin llenar un registro familiar."
    )
    st.subheader("Estado académico")
    st.caption("Las entregas internas se muestran con su alcance real de integración.")
    st.dataframe(pd.DataFrame(INTEGRACIONES), hide_index=True, use_container_width=True)
    st.info("El matching usa el motor Python canónico. Los simuladores muestran resultados sintéticos y beneficio neto sólo con costo conocido.")

def _render_privacidad():
    carpeta = Path(__file__).resolve().parents[2] / "cliente_flutter/assets/privacidad"
    aviso = json.loads((carpeta / "aviso.json").read_text(encoding="utf-8"))
    st.header("Privacidad y uso de datos")
    for bloque in aviso["bloques"]:
        with st.container(border=True):
            st.subheader(bloque["titulo"])
            st.write(bloque["texto"])
    st.markdown(f"**{aviso['titulo']}**")
    st.caption(f"Versión {aviso['version']} · {aviso['estado']}")
    st.download_button("Descargar aviso (PDF)", (carpeta / aviso["archivo"]).read_bytes(),
                       file_name=aviso["archivo"], mime="application/pdf")


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
    if "seccion_activa" not in st.session_state:
        st.session_state["seccion_activa"] = "Inicio"
    pagina = st.session_state["seccion_activa"]
    _render_navegacion(pagina)
    if pagina == "Inicio":
        _render_inicio()
    elif pagina == "Mapa":
        from cuidado.ui.mapa_alcaldias import mostrar_mapa_alcaldias

        st.info("Elige una alcaldía. Los puntos representan sedes reales de cuidado. Las cifras de población son indicadores agregados por alcaldía.")
        mostrar_mapa_alcaldias()
    elif pagina == "Comparar":
        from cuidado.ui.mapa_alcaldias import mostrar_comparativo_alcaldias

        st.info("Sedes con horario publicado indica qué proporción de centros documentó su horario. La disponibilidad de lugares requiere información de vacantes con fecha.")
        mostrar_comparativo_alcaldias()
    elif pagina == "Propuesta pública":
        _render_propuesta_publica()
    elif pagina == "Alianza público privada":
        _render_alianza_publico_privada()
    elif pagina == "Privacidad":
        _render_privacidad()
    else:
        _render_proyecto()
