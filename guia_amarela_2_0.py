import streamlit as st
from streamlit_folium import st_folium
import folium
import geopandas as gpd
import pandas as pd
import plotly.express as px

# Carregamento dos dados
url_lotes = "https://raw.githubusercontent.com/BryanSprenger/Trabalho-Final/main/lotes4.geojson"

# Carrega o GeoDataFrame
gdf = gpd.read_file(url_lotes)

# --- Configuração da Página Streamlit ---
st.set_page_config(page_title="Guia Amarela Interativa", page_icon=":scroll:", layout="centered")

st.title("Guia Amarela Interativa")
st.markdown("Selecione um lote no mapa ou filtre pela inscrição fiscal para visualizar os dados urbanísticos.")

# --- Criação do Mapa Base Folium ---
m = folium.Map(location=[-25.46, -49.27], zoom_start=12, tiles="CartoDB positron")

# Adiciona a camada GeoJSON
folium.GeoJson(
    gdf,
    name="Lotes",
    tooltip=folium.GeoJsonTooltip(
        fields=gdf.columns.tolist(),
        aliases=gdf.columns.tolist(),
        sticky=True
    )
).add_to(m)

folium.LayerControl().add_to(m)

# --- Renderização do Mapa no Streamlit ---
st_data = st_folium(m)
