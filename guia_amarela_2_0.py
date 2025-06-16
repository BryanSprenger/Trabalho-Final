import streamlit as st
import folium
from streamlit_folium import st_folium
import geopandas as gpd
from folium import GeoJson # Importação mantida, mas não estritamente necessária se apenas folium.GeoJson for usado

# --- Configuração da Página Streamlit ---
st.set_page_config(page_title="Guia Amarela Interativa", page_icon=":scroll:", layout="centered")

st.title("Guia Amarela Interativa")
st.markdown("Selecione um lote no mapa ou filtre pela inscrição fiscal para visualizar os dados urbanísticos.")

# --- Criação do Mapa Base Folium ---
m = folium.Map(location=[-25.46, -49.27], zoom_start=12, tiles="CartoDB positron")

# --- Adição de Controle de Camadas ---
folium.LayerControl().add_to(m)

# --- Renderização do Mapa no Streamlit ---
m

