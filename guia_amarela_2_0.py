import streamlit as st
import folium
from streamlit_folium import st_folium
import geopandas as gpd
from folium import GeoJson # Importação mantida, mas não estritamente necessária se apenas folium.GeoJson for usado

# --- Configuração da Página Streamlit ---
st.set_page_config(page_title="Guia Amarela Interativa", page_icon=":scroll:", layout="centered")

st.title("Guia Amarela Interativa")
st.markdown("Selecione um lote no mapa ou filtre pela inscrição fiscal para visualizar os dados urbanísticos.")

# --- URL do GeoJSON ---
url_lotes = "https://raw.githubusercontent.com/BryanSprenger/Trabalho-Final/main/lotes4.geojson"

# --- Carregamento e Verificação do GeoDataFrame ---
# Adiciona um bloco try-except para lidar com possíveis erros no carregamento do GeoJSON
try:
    gdf = gpd.read_file(url_lotes)
    st.success("GeoJSON carregado com sucesso!")
    
    # Exibe informações sobre o GeoDataFrame para depuração
    # Isso pode ajudar a identificar se há colunas ausentes ou inesperadas
    st.write("Colunas detectadas no GeoDataFrame:")
    st.dataframe(gdf.columns.tolist())
    
    st.write("Primeiras 5 linhas do GeoDataFrame (para verificar os dados):")
    st.dataframe(gdf.head())

except Exception as e:
    st.error(f"Erro ao carregar o GeoJSON da URL: {e}")
    st.warning("Verifique se a URL do GeoJSON está correta e se o arquivo está acessível e bem formatado.")
    st.stop() # Interrompe a execução se o GeoJSON não puder ser carregado

# --- Criação do Mapa Base Folium ---
m = folium.Map(location=[-25.46, -49.27], zoom_start=12, tiles="CartoDB positron")

# --- Adição da Camada GeoJSON ao Mapa ---
# A criação do tooltip é o ponto mais provável para o erro "value in keys"
# se as propriedades nas features do GeoJSON não corresponderem exatamente às colunas do gdf.
try:
    geojson_layer = folium.GeoJson(
        gdf,
        name="Lotes",
        # Gerar tooltip com base nas colunas do GeoDataFrame
        # Atenção: Todas as feições no GeoJSON devem ter as propriedades correspondentes a estas colunas.
        tooltip=folium.GeoJsonTooltip(fields=gdf.columns.tolist(), aliases=gdf.columns.tolist(), sticky=True)
    ).add_to(m)
    st.info("Camada GeoJSON adicionada ao mapa.")

except Exception as e:
    st.error(f"Erro ao adicionar a camada GeoJSON ou criar o tooltip: {e}")
    st.warning("Isso pode ser causado por inconsistências nos dados do GeoJSON (propriedades ausentes ou nulas).")
    st.stop() # Interrompe a execução se houver erro na camada GeoJSON

# --- Adição de Controle de Camadas ---
folium.LayerControl().add_to(m)

# --- Renderização do Mapa no Streamlit ---
# Esta linha estava faltando no seu script completo, mas estava no traceback
st_data = st_folium(m, width=1000, height=600)

# --- Exibir Dados do Lote Selecionado (Exemplo) ---
# O dicionário 'st_data' conterá informações sobre interações com o mapa,
# como o último clique ou o polígono selecionado.
if st_data and st_data.get("last_active_drawing"):
    drawing_type = st_data["last_active_drawing"].get("geometry", {}).get("type")
    if drawing_type == "Polygon":
        st.subheader("Lote Selecionado (Informações do Desenho):")
        st.json(st_data["last_active_drawing"])
    elif st_data.get("last_object_clicked"):
         st.subheader("Lote Clicado (Informações da Propriedade):")
         clicked_data = st_data["last_object_clicked"]
         # Tente exibir as propriedades da feição clicada
         if "properties" in clicked_data:
             st.json(clicked_data["properties"])
         else:
             st.write("Nenhuma propriedade encontrada para o objeto clicado.")
else:
    st.info("Clique ou desenhe no mapa para interagir.")
