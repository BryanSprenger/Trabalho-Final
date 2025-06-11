# app.py
import streamlit as st
import folium
from streamlit_folium import st_folium
import geopandas as gpd
from shapely.geometry import Polygon


# URL para o ZIP direto no GitHub
url_lotes = "https://raw.githubusercontent.com/BryanSprenger/Trabalho-Final/main/lotes.geojson"

polygons = gpd.read_file(url_lotes)

# Configuração da página
PAGE_CONFIG = {"page_title":" Guia Amarela Interativa", "page_icon":":scroll:", "layout":"centered"}
st.set_page_config(**PAGE_CONFIG)

st.markdown("Selecione um lote no mapa ou filtre pela inscrição fiscal para visualizar os dados urbanísticos.")

# Mapa base
m = folium.Map(location=[-25.46, -49.27], zoom_start=12, tiles='CartoDB positron', data=polygons)
folium.LayerControl().add_to(m)
folium_static(m)


# Exibe o mapa
st_data = st_folium(m, width=1000, height=500)

