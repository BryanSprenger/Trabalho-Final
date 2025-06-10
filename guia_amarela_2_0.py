# app.py
import streamlit as st
import folium
from streamlit_folium import st_folium
import geopandas as gpd
from shapely.geometry import Polygon

# Caminho local no ambiente do Streamlit (caso o zip esteja na pasta do projeto)
shapefile_path = "lotes_curitiba.zip"

# Carrega o GeoDataFrame a partir do zip
gdf = gpd.read_file(f"zip://{os.path.abspath(lotes.zip)}")

# Interface do Streamlit
st.set_page_config(layout="wide")
st.title("📍 Guia Amarela Interativa")

st.markdown("Selecione um lote no mapa ou filtre pela inscrição fiscal para visualizar os dados urbanísticos.")

# Mapa base
m = folium.Map(location=[-25.46, -49.27], zoom_start=12, tiles='CartoDB positron')

# Adiciona os lotes
for idx, row in gdf.iterrows():
    folium.GeoJson(
        row["geometry"],
        name=f"Lote {row['inscricao_fiscal']}",
        tooltip=f"Inscrição Fiscal: {row['inscricao_fiscal']}",
        popup=folium.Popup(f"""
            <b>Inscrição Fiscal:</b> {row['inscricao_fiscal']}<br>
            <b>Taxa de Ocupação:</b> {row['taxa_ocupacao']}<br>
            <b>Coef. Aproveitamento:</b> {row['coeficiente_aproveitamento']}<br>
            <b>Uso Permitido:</b> {row['uso_permitido']}
        """, max_width=300)
    ).add_to(m)

# Exibe o mapa
st_data = st_folium(m, width=1000, height=500)

