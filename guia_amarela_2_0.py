import streamlit as st
from streamlit_folium import st_folium
import folium
import geopandas as gpd
import pandas as pd
import plotly.express as px

# Carregamento dos dados
url_lotes = "https://raw.githubusercontent.com/BryanSprenger/Trabalho-Final/main/Lotes2021_4.geojson"

# Carrega o GeoDataFrame
gdf = gpd.read_file(url_lotes)
gdf = gdf[gdf.is_valid & ~gdf.geometry.is_empty]

# --- Configuração da Página Streamlit ---
st.set_page_config(page_title="Guia Amarela Interativa", page_icon=":scroll:", layout="wide")

st.title("Guia Amarela Interativa")
st.markdown("Selecione um lote no mapa ou filtre pela inscrição fiscal para visualizar os dados urbanísticos.")

# --- Criação do Mapa Base Folium ---
m = folium.Map(location=[-25.46, -49.27], zoom_start=12, tiles="CartoDB positron")

# Adiciona a camada GeoJSON
campos_seguro = ["CDLOTE", "INDFISCAL", "CDVIA", "NMVIA"]  # substitua por campos que existam de verdade

folium.GeoJson(
    gdf,
    name="Lotes",
    tooltip=folium.GeoJsonTooltip(
        fields=campos_seguro,
        aliases=["Código da Via", "Indicação Fiscal", "Código da Via", "Nome da Via"],
        sticky=True
    )
).add_to(m)

folium.LayerControl().add_to(m)

# --- Renderização do Mapa no Streamlit ---
st_data = st_folium(m, width="100%", height=700)
