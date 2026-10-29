"""Mapa interactivo y panel de detalle del explorador territorial."""

from __future__ import annotations

import html

import folium
import pandas as pd
import streamlit as st
from streamlit_folium import st_folium

from cuidado.services.mapa_alcaldias import (
    cargar_mapa_alcaldias,
    claves_alcaldias,
    fila_indicador,
    indicadores_de_alcaldia,
    indicadores_publicos,
    nombre_alcaldia,
)


COLOR_MAPA = "#EDE9FE"
COLOR_BORDE = "#CBD5E1"
COLOR_SELECCION = "#6D28D9"
COLOR_TEXTO = "#172033"
AGE_INDICATORS = [
    "pob_0_4",
    "pob_5_9",
    "pob_10_14",
    "pob_15_19",
    "pob_20_24",
    "pob_25_29",
    "pob_30_34",
    "pob_35_39",
    "pob_40_44",
    "pob_45_49",
    "pob_50_54",
    "pob_55_59",
    "pob_60_64",
    "pob_65_69",
    "pob_70_74",
    "pob_75_79",
    "pob_80_84",
    "pob_85_plus",
    "pob_unknown",
]


def _crear_mapa(geometria, clave_seleccionada: str | None) -> folium.Map:
    min_longitud, min_latitud, max_longitud, max_latitud = geometria.total_bounds
    mapa = folium.Map(
        location=[(min_latitud + max_latitud) / 2, (min_longitud + max_longitud) / 2],
        tiles=None,
        zoom_control=True,
        control_scale=True,
    )
    mapa.fit_bounds([[min_latitud, min_longitud], [max_latitud, max_longitud]])
    for _, fila in geometria.iterrows():
        clave = str(fila["clave"])
        nombre = nombre_alcaldia(clave) or str(fila["alcaldia"]).title()
        seleccionada = clave == clave_seleccionada
        folium.GeoJson(
            data={
                "type": "Feature",
                "geometry": fila.geometry.__geo_interface__,
                "properties": {"clave": clave, "nombre": nombre},
            },
            name=nombre,
            embed=True,
            style_function=lambda _, selected=seleccionada: {
                "fillColor": COLOR_MAPA if not selected else "#D8C8FA",
                "color": COLOR_SELECCION if selected else COLOR_BORDE,
                "weight": 3 if selected else 1,
                "fillOpacity": 0.9,
            },
            highlight_function=lambda _: {
                "color": COLOR_SELECCION,
                "weight": 3,
                "fillOpacity": 0.95,
            },
            tooltip=folium.GeoJsonTooltip(
                fields=["nombre"],
                aliases=["Alcaldía"],
                labels=False,
                localize=False,
                style=(
                    "background-color: white; color: #172033; "
                    "font-family: sans-serif; font-size: 13px; padding: 8px;"
                ),
                sticky=True,
                opacity=0.95,
            ),
        ).add_to(mapa)
    return mapa


def _valor_texto(fila: pd.Series | None) -> str:
    if fila is None or pd.isna(fila["valor"]):
        return "Dato no disponible"
    valor = float(fila["valor"])
    if fila["unidad"] == "%":
        return f"{valor:,.1f}%"
    return f"{valor:,.0f} {fila['unidad']}"


def _tarjeta_indicador(titulo: str, fila: pd.Series | None, nota: str = "") -> None:
    valor = _valor_texto(fila)
    periodo = "Periodo por verificar" if fila is None or fila["periodo"] == "no documentado" else fila["periodo"]
    estado = " · estimación" if fila is not None and fila["tipo"] == "estimado" else ""
    nota_html = f'<div class="territorial-kpi-note">{html.escape(nota)}</div>' if nota else ""
    st.markdown(
        f'<div class="territorial-kpi"><div class="territorial-kpi-label">{html.escape(titulo)}</div>'
        f'<div class="territorial-kpi-value">{valor}</div>'
        f'<div class="territorial-kpi-meta">{periodo}{estado}</div>'
        f"{nota_html}</div>",
        unsafe_allow_html=True,
    )


def _fila_60_mas(indicadores: pd.DataFrame, clave: str) -> pd.Series | None:
    filas = indicadores_de_alcaldia(indicadores, clave)
    ids = ["pob_60_64", "pob_65_69", "pob_70_74", "pob_75_79", "pob_80_84", "pob_85_plus"]
    seleccion = filas.loc[filas["id_indicador"].isin(ids)]
    valores = pd.to_numeric(seleccion["valor"], errors="coerce")
    if len(seleccion) != len(ids) or valores.isna().any():
        return None
    resultado = seleccion.iloc[0].copy()
    resultado["valor"] = valores.sum()
    resultado["unidad"] = "personas"
    resultado["periodo"] = "no documentado"
    resultado["tipo"] = "observado"
    return resultado


def _grafico_edades(indicadores: pd.DataFrame, clave: str) -> None:
    filas = indicadores_de_alcaldia(indicadores, clave)
    edades = filas.loc[filas["id_indicador"].isin(AGE_INDICATORS), ["id_indicador", "valor", "poblacion"]].copy()
    if edades.empty:
        st.info("No hay grupos de edad disponibles para esta alcaldía.")
        return
    edades["valor"] = pd.to_numeric(edades["valor"], errors="coerce")
    edades = edades.dropna(subset=["valor"])
    edades["grupo"] = edades["poblacion"].fillna(edades["id_indicador"])
    st.vega_lite_chart(
        edades,
        {
            "mark": {"type": "bar", "color": "#6D28D9"},
            "encoding": {
                "y": {"field": "grupo", "type": "nominal", "sort": "-x", "title": None},
                "x": {"field": "valor", "type": "quantitative", "title": "Personas"},
                "tooltip": [
                    {"field": "grupo", "type": "nominal", "title": "Grupo"},
                    {"field": "valor", "type": "quantitative", "title": "Personas", "format": ",.0f"},
                ],
            },
            "height": {"step": 23},
            "config": {"axis": {"labelColor": COLOR_TEXTO, "titleColor": COLOR_TEXTO}},
        },
        use_container_width=True,
    )
    tabla = edades.rename(columns={"grupo": "Grupo de edad", "valor": "Personas"})[
        ["Grupo de edad", "Personas"]
    ]
    tabla["Personas"] = tabla["Personas"].map(lambda valor: f"{valor:,.0f}")
    st.dataframe(tabla, hide_index=True, use_container_width=True)


def mostrar_mapa_alcaldias() -> None:
    """Renderiza el mapa, selector y panel de una única alcaldía seleccionada."""

    try:
        geometria, indicadores, catalogo, fuentes = cargar_mapa_alcaldias("v3")
    except (FileNotFoundError, ValueError) as error:
        st.error(f"No se puede cargar el explorador territorial: {error}")
        return

    st.markdown('<div class="section-kicker">Explorador territorial</div>', unsafe_allow_html=True)
    st.header("Mapa por alcaldía")
    st.markdown(
        '<div class="section-card">Selecciona una alcaldía para consultar sus datos. '
        "Los polígonos corresponden al recurso oficial de límites de alcaldías "
        "del Portal de Datos Abiertos de CDMX.</div>",
        unsafe_allow_html=True,
    )
    st.warning(
        "La población corresponde al Censo 2020 de INEGI (ITER), agregada por alcaldía. "
        "Los grupos etarios describen población registrada y no equivalen a necesidad de cuidado."
    )
    claves = claves_alcaldias(geometria)
    if "mapa_alcaldia_pending" in st.session_state:
        st.session_state["mapa_alcaldia_selector"] = st.session_state.pop("mapa_alcaldia_pending")
    if "mapa_alcaldia_selector" not in st.session_state:
        st.session_state["mapa_alcaldia_selector"] = ""
    seleccion = st.selectbox(
        "Alcaldía",
        [""] + claves,
        key="mapa_alcaldia_selector",
        format_func=lambda clave: "Selecciona una alcaldía" if not clave else nombre_alcaldia(clave),
    )
    if st.button("Ver toda CDMX", key="mapa_alcaldia_reset"):
        st.session_state["mapa_alcaldia_pending"] = ""
        st.rerun()

    st.caption(
        "El mapa inicia con las 16 alcaldías en lavanda uniforme. Puedes seleccionar "
        "mediante la lista o haciendo clic en un polígono."
    )
    mapa = _crear_mapa(geometria, seleccion or None)
    evento = st_folium(
        mapa,
        key=f"mapa-alcaldias-{seleccion or 'todas'}",
        height=420,
        use_container_width=True,
        returned_objects=["last_active_drawing"],
    )
    dibujo = evento.get("last_active_drawing") if evento else None
    clave_clic = (dibujo or {}).get("properties", {}).get("clave")
    if clave_clic in claves and clave_clic != seleccion:
        st.session_state["mapa_alcaldia_pending"] = clave_clic
        st.rerun()

    if not seleccion:
        st.info("Selecciona una alcaldía para consultar sus datos.")
        return

    nombre = nombre_alcaldia(seleccion)
    st.markdown(f'<div class="section-card"><h2>Datos de {nombre}</h2>'
                '<p class="territorial-status">Fuente: INEGI, Censo 2020 (ITER). '
                'Cartografía: Portal de Datos Abiertos de CDMX.</p></div>',
                unsafe_allow_html=True)
    st.subheader("Indicadores disponibles")
    tarjetas = [
        ("Población total", fila_indicador(indicadores, seleccion, "poblacion_total"), ""),
        ("Población de 0 a 4 años", fila_indicador(indicadores, seleccion, "pob_0_4"), "Intervalo exacto disponible."),
        ("Personas de 60 años o más", _fila_60_mas(indicadores, seleccion), "Suma técnica de grupos etarios; no equivale a necesidad de cuidado."),
    ]
    columnas = st.columns(4)
    for columna, (titulo, fila, nota) in zip(columnas, tarjetas):
        with columna:
            _tarjeta_indicador(titulo, fila, nota)

    st.subheader("Población por grupos de edad")
    st.caption("Los grupos son mutuamente excluyentes según la fuente. Edad no especificada se conserva sin redistribuir.")
    indicadores_autorizados = indicadores_publicos(indicadores, catalogo)
    _grafico_edades(indicadores_autorizados, seleccion)
    st.markdown(
        '<div class="section-card"><strong>Interpretación:</strong> estos conteos '
        "describen la población registrada y no prueban necesidad de cuidado, demanda efectiva, "
        "abandono laboral ni impacto social. La suma de 0–14 y 60+ no debe leerse como una "
        "población única sin solapamientos.</div>",
        unsafe_allow_html=True,
    )
    st.subheader("Fuentes y límites")
    for fuente in fuentes:
        st.caption(
            f"{fuente['titulo']} · {fuente['institucion']} · "
            f"Periodo: {fuente['periodo_dato']}. URL no documentada en el repositorio."
        )
    st.dataframe(
        indicadores_de_alcaldia(indicadores_autorizados, seleccion)[
            ["id_indicador", "valor", "unidad", "periodo", "tipo", "estado_disponibilidad"]
        ].rename(
            columns={
                "id_indicador": "Indicador",
                "valor": "Valor",
                "unidad": "Unidad",
                "periodo": "Periodo",
                "tipo": "Tipo",
                "estado_disponibilidad": "Estado",
            }
        ),
        hide_index=True,
        use_container_width=True,
    )


def mostrar_comparativo_alcaldias() -> None:
    """Compara únicamente indicadores demográficos autorizados."""

    try:
        _, indicadores, catalogo, _ = cargar_mapa_alcaldias("v3")
    except (FileNotFoundError, ValueError) as error:
        st.error(f"No se puede cargar el comparativo territorial: {error}")
        return
    autorizados = indicadores_publicos(indicadores, catalogo)
    opciones = ["poblacion_total", "pob_0_4"]
    nombres = {"poblacion_total": "Población total", "pob_0_4": "Población de 0 a 4 años"}
    indicador = st.selectbox(
        "Indicador demográfico autorizado",
        opciones,
        format_func=nombres.get,
        key="comparativo_mapa_indicador",
    )
    tabla = autorizados.loc[autorizados["id_indicador"].eq(indicador),
                            ["clave_alcaldia", "alcaldia", "valor", "unidad", "periodo"]]
    tabla = tabla.sort_values("valor", ascending=False).reset_index(drop=True)
    tabla.insert(0, "Posición", range(1, len(tabla) + 1))
    tabla = tabla.rename(columns={"clave_alcaldia": "Clave", "alcaldia": "Alcaldía",
                                  "valor": "Valor", "unidad": "Unidad",
                                  "periodo": "Periodo"})
    st.markdown(
        '<div class="section-card">El orden corresponde al indicador seleccionado; '
        "no representa una evaluación general de la alcaldía.</div>",
        unsafe_allow_html=True,
    )
    st.dataframe(tabla, hide_index=True, use_container_width=True)
