import streamlit as st
from streamlit_folium import st_folium
import folium
import geopandas as gpd
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Carregamento dos dados
    url_lotes = "https://raw.githubusercontent.com/BryanSprenger/Trabalho-Final/main/Lotes2021_4.geojson"

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

    # Carrega o arquivo GeoJSON localmente
    gdf = gpd.read_file(url_lotes)

    # Caixa de entrada para Indicação Fiscal
    ind_fiscal = st.text_input("Digite a Indicação Fiscal (INDFISCAL):")

    # Verifica se foi digitado algo
    if ind_fiscal:
        # Filtra o lote correspondente
        lote_filtrado = gdf[gdf["INDFISCAL"] == ind_fiscal]

        if lote_filtrado.empty:
            st.warning("Nenhum lote encontrado com essa indicação fiscal.")
        else:
            lote = lote_filtrado.geometry.values[0]

            # Se for multipolígono, pega o primeiro
            if lote.geom_type == "MultiPolygon":
                lote = list(lote.geoms)[0]

            x, y = lote.exterior.coords.xy
            z_base = [0] * len(x)
            area = lote.area

            ca = st.slider("Coeficiente de Aproveitamento (CA)", 0.5, 4.0, 2.0, 0.1)
            altura = (ca * area) / (area ** 0.5)
            z_top = [altura] * len(x)

            fig = go.Figure()

            # base
            fig.add_trace(go.Scatter3d(x=x, y=y, z=z_base, mode='lines',
                                       line=dict(color='blue', width=4), name='Base'))

            # topo
            fig.add_trace(go.Scatter3d(x=x, y=y, z=z_top, mode='lines',
                                       line=dict(color='lightblue', width=4), name='Topo'))

            for i in range(len(x)):
                fig.add_trace(go.Scatter3d(
                    x=[x[i], x[i]], y=[y[i], y[i]], z=[0, altura],
                    mode='lines', line=dict(color='lightblue', width=2), showlegend=False
                ))

            fig.update_layout(
                scene=dict(xaxis_title='X', yaxis_title='Y', zaxis_title='Altura (m)'),
                margin=dict(l=0, r=0, b=0, t=30)
            )

            st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Insira a Indicação Fiscal para visualizar o lote.")

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
