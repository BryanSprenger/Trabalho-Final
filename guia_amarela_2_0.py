# app.py
import streamlit as st
import folium
from streamlit_folium import st_folium
import geopandas as gpd
from folium import GeoJson

# Configuração da página
st.set_page_config(page_title="Guia Amarela Interativa", page_icon=":scroll:", layout="centered")

st.title("Guia Amarela Interativa")
st.markdown("Selecione um lote no mapa ou filtre pela inscrição fiscal para visualizar os dados urbanísticos.")

# URL do GeoJSON no GitHub
url_lotes = "https://raw.githubusercontent.com/BryanSprenger/Trabalho-Final/main/lotes4.geojson"

# Carrega o GeoDataFrame
gdf = gpd.read_file(url_lotes)

# Remove colunas com dados que não são serializáveis (objetos complexos, listas, etc.)
serializable_cols = []
for col in gdf.columns:
    try:
        _ = gdf[col].iloc[0]
        json_test = pd.Series([gdf[col].iloc[0]]).to_json()
        serializable_cols.append(col)
    except:
        pass

# Cria o mapa base
m = folium.Map(location=[-25.46, -49.27], zoom_start=12, tiles="CartoDB positron")

# Adiciona a camada GeoJSON ao mapa
geojson_layer = folium.GeoJson(
    gdf,
    name="Lotes",
    tooltip=folium.GeoJsonTooltip(fields=gdf.columns.tolist(), aliases=gdf.columns.tolist(), sticky=True)
).add_to(m)

folium.LayerControl().add_to(m)

# Exibe o mapa no Streamlit
st_data = st_folium(m, width=1000, height=600)
