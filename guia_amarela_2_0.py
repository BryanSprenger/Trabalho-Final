# app.py
import streamlit as st
import folium
from streamlit_folium import st_folium
import geopandas as gpd
from shapely.geometry import Polygon

# Simula dados de dois lotes
data = {
    "inscricao_fiscal": ["123456", "789012"],
    "taxa_ocupacao": [0.6, 0.5],
    "coeficiente_aproveitamento": [2.0, 1.5],
    "uso_permitido": ["Residencial", "Comercial"],
    "geometry": [
        Polygon([(-49.27, -25.44), (-49.27, -25.4395), (-49.2695, -25.4395), (-49.2695, -25.44)]),
        Polygon([(-49.269, -25.44), (-49.269, -25.4395), (-49.2685, -25.4395), (-49.2685, -25.44)])
    ]
}

# Cria o GeoDataFrame
gdf = gpd.GeoDataFrame(data, crs="EPSG:4326")

# Interface do Streamlit
st.set_page_config(layout="wide")
st.title("📍 Guia Amarela Interativa")

st.markdown("Selecione um lote no mapa ou filtre pela inscrição fiscal para visualizar os dados urbanísticos.")

# Mapa base
m = folium.Map(location=[-25.43975, -49.2695], zoom_start=18)

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

