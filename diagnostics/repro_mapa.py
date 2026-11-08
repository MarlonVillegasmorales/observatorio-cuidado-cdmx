"""Reproducción local mínima del componente Folium.

Este archivo no forma parte de la navegación pública. Ejecútalo con:

    python -m streamlit run diagnostics/repro_mapa.py
"""

import folium
import streamlit as st
from streamlit_folium import st_folium


st.set_page_config(page_title="Diagnóstico Folium")
st.header("Reproducción mínima de streamlit-folium")
st.caption("Mapa sin datos territoriales, estilos personalizados ni callbacks.")

mapa = folium.Map(location=[19.4326, -99.1332], zoom_start=10)
st_folium(
    mapa,
    key="diagnostico-mapa-minimo",
    height=420,
    returned_objects=["last_clicked"],
)
