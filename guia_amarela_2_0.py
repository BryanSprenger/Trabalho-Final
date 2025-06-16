import streamlit as st
from streamlit_folium import folium_static
import folium
import geopandas as gpd
import pandas as pd
import plotly.express as px

# Carregamento dos dados



# --- Configuração da Página Streamlit ---
st.set_page_config(page_title="Guia Amarela Interativa", page_icon=":scroll:", layout="centered")

st.title("Guia Amarela Interativa")
st.markdown("Selecione um lote no mapa ou filtre pela inscrição fiscal para visualizar os dados urbanísticos.")

# --- Criação do Mapa Base Folium ---
m = folium.Map(location=[-25.46, -49.27], zoom_start=12, tiles="CartoDB positron")


# --- Renderização do Mapa no Streamlit ---
folium_static(m)
