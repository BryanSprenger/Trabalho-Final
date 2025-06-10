# app.py
import streamlit as st
import folium
from streamlit_folium import st_folium
import geopandas as gpd
from shapely.geometry import Polygon

# URL para o ZIP direto no GitHub
url = "https://raw.githubusercontent.com/BryanSprenger/Trabalho-Final/main/lotes.zip"

# Faz o download do arquivo zip
response = requests.get(url)
with zipfile.ZipFile(io.BytesIO(response.content)) as z:
    z.extractall("temp_shp")  # extrai os arquivos numa pasta temporária

# Agora carregamos o shapefile da pasta extraída
gdf = gpd.read_file("temp_shp")  # o geopandas identifica automaticamente o .shp

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

