"""Capa documental compartida con el explorador móvil."""
import html
import json
from pathlib import Path

import folium
import streamlit as st

ARCHIVO = Path(__file__).resolve().parents[2] / "cliente_flutter/assets/data/directorio_infantil.json"


@st.cache_data
def cargar_directorio(version):
    return json.loads(ARCHIVO.read_text(encoding="utf8"))


def agregar_puntos(mapa, grupos):
    for grupo in grupos:
        for sede in grupo["sedes"]:
            if punto := sede.get("punto"):
                nombres = " / ".join(u["nombre"] for u in sede["unidades"])
                folium.CircleMarker(punto, radius=4, color="#075e55", fill=True,
                                    fill_opacity=0.85, tooltip=html.escape(nombres)).add_to(mapa)


def mostrar_directorio(grupos, clave):
    seleccion = [grupos[clave]] if clave else list(grupos.values())
    resumen = {k: sum(g["resumen"][k] for g in seleccion) for k in seleccion[0]["resumen"]}
    st.subheader("Oferta infantil documentada")
    st.write(f"{resumen['sedes_unicas']} sedes · {resumen['con_horario']} con horario · "
             f"{resumen['con_capacidad_exacta']} con capacidad exacta · "
             f"{resumen['con_rango_o_tope']} con rango o límite · "
             f"{resumen['con_vacantes_fechadas']} con vacantes fechadas")
    sedes = [s for g in seleccion for s in g["sedes"]]
    st.caption(f"{sum('punto' in s for s in sedes)} sedes con coordenadas. "
               "Los horarios y capacidades corresponden al periodo de cada fuente.")
    if not clave:
        return
    with st.expander("Consultar sedes y fuentes"):
        unidades = [u for s in sedes for u in s["unidades"]]
        red = st.selectbox("Red de cuidado", ["Todas"] + sorted({u["red"] for u in unidades}), key=f"red_{clave}")
        opciones = [u for u in unidades if red == "Todas" or u["red"] == red]
        idx = st.selectbox("Centro", range(len(opciones)), format_func=lambda i: opciones[i]["nombre"] + " · " + opciones[i]["domicilio"], key=f"centro_{clave}_{red}")
        u = opciones[idx]
        st.write(u["red"], "·", u["domicilio"])
        if "apertura" in u:
            st.write(f"Horario {u['apertura']}–{u['cierre']} · {u['periodo_horario']}")
        if "apertura_extra" in u:
            st.write(f"Horario extraordinario {u['apertura_extra']}–{u['cierre_extra']}")
        cap = u.get("capacidad_exacta") or (f"{u['capacidad_min']}–{u['capacidad_max']}" if "capacidad_min" in u else f"hasta {u['capacidad_max']}" if "capacidad_max" in u else None)
        if cap:
            st.write(f"Capacidad {cap} · {u['periodo_capacidad']}")
        st.write(f"Vacantes: {u['vacantes']} · {u['fecha_vacantes']}" if u.get("fecha_vacantes") else "Vacantes: sin dato fechado")
        st.markdown(f"[Fuente del directorio]({u['fuente_url']}) · {u['periodo_fuente']}")
        if "fuente_capacidad_url" in u:
            st.markdown(f"[Fuente de capacidad]({u['fuente_capacidad_url']})")
        if u.get("nota"):
            st.caption(u["nota"])
