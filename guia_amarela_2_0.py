import streamlit as st
from streamlit_folium import st_folium
import folium
import geopandas as gpd
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go



# --- Configuração da Página Streamlit ---
st.set_page_config(page_title="Guia Amarela Interativa", page_icon=":scroll:", layout="wide")

st.title("Guia Amarela Interativa")
st.markdown("Selecione um lote no mapa ou filtre pela inscrição fiscal para visualizar os dados urbanísticos.")

# Menu lateral
st.sidebar.title("Navegação")
pagina = st.sidebar.radio(
    "Selecione uma seção:",
    ("🏠 Home", "🏗️ Potencial Construtivo", "📐 Área de Ocupação", "📊 Indicadores Urbanísticos", "🗺️ Mapa Interativo")
)

# --- HOME ---
if pagina == "🏠 Home":
    st.title("Guia Amarela Interativa")
    st.markdown("""
    Esta aplicação visa apresentar as informações da Consulta Informativa de Lote (CIL), também conhecida como Guia Amarela, de forma interativa, visual e acessível.

    **Funcionalidades principais:**
    - Visualização de parâmetros urbanísticos de forma gráfica
    - Mapa interativo do lote
    - Simulação de potencial construtivo em 3D
    - Explicações sobre zoneamento, coeficiente de aproveitamento, recuos, etc.
    """)

# --- POTENCIAL CONSTRUTIVO ---
elif pagina == "🏗️ Potencial Construtivo":
    st.title("Potencial Construtivo")

    st.markdown("Visualize aqui o volume máximo permitidos pelo coeficiente de aproveitamento, altura e recuos mínimos.")

    # Slider lateral
    ca = st.sidebar.slider("Coeficiente de Aproveitamento (CA)", 0.5, 6.0, 1.5, 0.1)
    area_lote = st.sidebar.number_input("Área do Lote (m²)", min_value=50.0, value=360.0, step=10.0)
    altura_max = st.sidebar.number_input("Altura Máxima (m)", min_value=3.0, value=12.0, step=1.0)

    area_construida_max = ca * area_lote
    base_area = area_lote ** 0.5
    altura_predio = min(altura_max, area_construida_max / base_area)

    # Visualização 3D simplificada
    fig = go.Figure(data=[
        go.Mesh3d(
            x=[0, base_area, base_area, 0, 0, base_area, base_area, 0],
            y=[0, 0, base_area, base_area, 0, 0, base_area, base_area],
            z=[0, 0, 0, 0, altura_predio, altura_predio, altura_predio, altura_predio],
            color='lightblue', opacity=0.6
        )
    ])
    fig.update_layout(
        title="Volume Máximo Simulado",
        scene=dict(xaxis_title='X (m)', yaxis_title='Y (m)', zaxis_title='Altura (m)'),
        margin=dict(l=0, r=0, b=0, t=30)
    )
    st.plotly_chart(fig, use_container_width=True)

# --- ÁREA DE OCUPAÇÃO ---
elif pagina == "📐 Área de Ocupação":
    st.title("Área de Ocupação do Lote")

    st.markdown("Visualize o quanto do lote pode ou não ser ocupado, com base na taxa de ocupação e permeabilidade.")

    area_lote = st.sidebar.number_input("Área do lote (m²):", min_value=50.0, value=360.0)
    taxa_ocupacao = st.sidebar.slider("Taxa de Ocupação (%)", 10, 100, 60)

    area_ocupada = (taxa_ocupacao / 100) * area_lote
    area_livre = area_lote - area_ocupada

    st.write(f"Área ocupada: {area_ocupada:.2f} m²")
    st.write(f"Área livre: {area_livre:.2f} m²")

    # Gráfico com Plotly
    import plotly.express as px
    df_ocupacao = px.data.tips()  # Substituído abaixo
    df_ocupacao = {
        "Tipo": ["Área Ocupada", "Área Livre"],
        "Valor": [area_ocupada, area_livre]
    }
    fig = px.pie(df_ocupacao, values="Valor", names="Tipo", title="Distribuição do Lote")
    st.plotly_chart(fig)

# --- INDICADORES ---
elif pagina == "📊 Indicadores Urbanísticos":
    st.title("Indicadores Urbanísticos")
    st.markdown("Apresenta valores de altura máxima, CA, recuos e outros parâmetros em formato de tabela ou gráfico.")

    # Exemplo fictício
    dados = {
        "Parâmetro": ["Altura Máxima", "CA", "Taxa de Ocupação", "Permeabilidade"],
        "Valor": ["12m", "1.5", "60%", "25%"],
        "Descrição": ["Limite de altura", "Coeficiente de aproveitamento", "Porcentagem máxima construída", "Área mínima permeável"]
    }
    import pandas as pd
    df = pd.DataFrame(dados)
    st.table(df)

# --- MAPA INTERATIVO ---
elif pagina == "🗺️ Mapa Interativo":
    st.title("Mapa Interativo")

    # Carregamento dos dados
    url_lotes = "https://raw.githubusercontent.com/BryanSprenger/Trabalho-Final/main/Lotes2021_4.geojson"

    # Carrega o GeoDataFrame
    gdf = gpd.read_file(url_lotes)
    gdf = gdf[gdf.is_valid & ~gdf.geometry.is_empty]

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
