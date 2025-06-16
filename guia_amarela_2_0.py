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
    m = folium.Map(location=[-25.5, -49.3], zoom_start=9)
    folium.Choropleth(
        geo_data=bairros_finais.to_json(),
        name='estacionamentos por bairro',
        data=bairros_finais,
        columns=['OBJECTID', 'num_pto'],
        key_on='feature.properties.OBJECTID',
        fill_color='YlGn',
        legend_name='Estacionamentos por bairro'
    ).add_to(m)
    folium.LayerControl().add_to(m)
    folium_static(m)

if __name__ == '__main__':
    main()

