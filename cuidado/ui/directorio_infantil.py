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
    st.write(f"De {resumen['sedes_unicas']} centros documentados, "
             f"{resumen['con_horario']} tienen un horario publicado.")
    with st.expander("Lugares y disponibilidad"):
        st.write(f"{resumen['con_capacidad_exacta']} centros publicaron cuántas personas podían atender "
                 f"y {resumen['con_rango_o_tope']} publicaron un rango o límite.")
        st.write(f"{resumen['con_vacantes_fechadas']} centros informaron lugares libres con fecha."
                 if resumen['con_vacantes_fechadas'] else "Todavía se desconoce cuántos lugares están libres.")
    if not clave:
        with st.expander("¿Cuántas personas cuidan en México?"):
            st.write("En México, 31.7 millones de personas de 15 años o más cuidaron a alguien de su hogar o de otro hogar en 2022. Entre quienes eran cuidadores principales, las mujeres dedicaron en promedio 39 horas por semana y los hombres, 31.")
            st.markdown("[INEGI · ENASIC 2022 · resultados nacionales](https://www.inegi.org.mx/programas/enasic/2022/)")
    with st.expander("Cómo protegemos tus datos"):
        st.write("Puedes consultar el mapa sin dar tu nombre ni tu ubicación. Los puntos representan centros de cuidado. El directorio publica domicilios institucionales y cifras por sede. Los datos de niñas, niños, familias y personas trabajadoras quedan fuera de este directorio.")
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
