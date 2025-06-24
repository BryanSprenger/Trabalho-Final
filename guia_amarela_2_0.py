import streamlit as st
from streamlit_folium import st_folium
import folium
import geopandas as gpd
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


url_lotes = "https://raw.githubusercontent.com/BryanSprenger/Trabalho-Final/main/Lotes2021_6.geojson"
gdf_lotes = gpd.read_file(url_lotes)
gdf_lotes = gdf_lotes[gdf_lotes.is_valid & ~gdf_lotes.geometry.is_empty]

    
#Carregando os relatórios de Alvará
# Mapeamento de anos para URLs dos arquivos CSV
urls_alvaras = {
    "2000": "https://raw.githubusercontent.com/BryanSprenger/Trabalho-Final/refs/heads/main/RELATORIOS/RELATORIO_2000.csv",
    "2001": "https://raw.githubusercontent.com/BryanSprenger/Trabalho-Final/refs/heads/main/RELATORIOS/RELATORIO_2001.csv",
    "2002": "https://raw.githubusercontent.com/BryanSprenger/Trabalho-Final/refs/heads/main/RELATORIOS/RELATORIO_2002.csv",
    "2003": "https://raw.githubusercontent.com/BryanSprenger/Trabalho-Final/refs/heads/main/RELATORIOS/RELATORIO_2003.csv",
    "2004": "https://raw.githubusercontent.com/BryanSprenger/Trabalho-Final/refs/heads/main/RELATORIOS/RELATORIO_2004.csv",
    "2005": "https://raw.githubusercontent.com/BryanSprenger/Trabalho-Final/refs/heads/main/RELATORIOS/RELATORIO_2005.csv",
    "2006": "https://raw.githubusercontent.com/BryanSprenger/Trabalho-Final/refs/heads/main/RELATORIOS/RELATORIO_2006.csv",
    "2007": "https://raw.githubusercontent.com/BryanSprenger/Trabalho-Final/refs/heads/main/RELATORIOS/RELATORIO_2007.csv",
    "2008": "https://raw.githubusercontent.com/BryanSprenger/Trabalho-Final/refs/heads/main/RELATORIOS/RELATORIO_2008.csv",
    "2009": "https://raw.githubusercontent.com/BryanSprenger/Trabalho-Final/refs/heads/main/RELATORIOS/RELATORIO_2009.csv",
    "2010": "https://raw.githubusercontent.com/BryanSprenger/Trabalho-Final/refs/heads/main/RELATORIOS/RELATORIO_2010.csv",
    "2011": "https://raw.githubusercontent.com/BryanSprenger/Trabalho-Final/refs/heads/main/RELATORIOS/RELATORIO_2011.csv",
    "2012": "https://raw.githubusercontent.com/BryanSprenger/Trabalho-Final/refs/heads/main/RELATORIOS/RELATORIO_2012.csv",
    "2013": "https://raw.githubusercontent.com/BryanSprenger/Trabalho-Final/refs/heads/main/RELATORIOS/RELATORIO_2013.csv",
    "2014": "https://raw.githubusercontent.com/BryanSprenger/Trabalho-Final/refs/heads/main/RELATORIOS/RELATORIO_2014.csv",
    "2015": "https://raw.githubusercontent.com/BryanSprenger/Trabalho-Final/refs/heads/main/RELATORIOS/RELATORIO_2015.csv",
    "2016": "https://raw.githubusercontent.com/BryanSprenger/Trabalho-Final/refs/heads/main/RELATORIOS/RELATORIO_2016.csv",
    "2017": "https://raw.githubusercontent.com/BryanSprenger/Trabalho-Final/refs/heads/main/RELATORIOS/RELATORIO_2017.csv",
    "2018": "https://raw.githubusercontent.com/BryanSprenger/Trabalho-Final/refs/heads/main/RELATORIOS/RELATORIO_2018.csv",
    "2019": "https://raw.githubusercontent.com/BryanSprenger/Trabalho-Final/refs/heads/main/RELATORIOS/RELATORIO_2019.csv",
    "2020": "https://raw.githubusercontent.com/BryanSprenger/Trabalho-Final/refs/heads/main/RELATORIOS/RELATORIO_2020.csv",
    "2021": "https://raw.githubusercontent.com/BryanSprenger/Trabalho-Final/refs/heads/main/RELATORIOS/RELATORIO_2021.csv",
    "2022": "https://raw.githubusercontent.com/BryanSprenger/Trabalho-Final/refs/heads/main/RELATORIOS/RELATORIO_2022.csv",
    "2023": "https://raw.githubusercontent.com/BryanSprenger/Trabalho-Final/refs/heads/main/RELATORIOS/RELATORIO_2023.csv",
    "2024": "https://raw.githubusercontent.com/BryanSprenger/Trabalho-Final/refs/heads/main/RELATORIOS/RELATORIO_2024.csv",
    "2025": "https://raw.githubusercontent.com/BryanSprenger/Trabalho-Final/refs/heads/main/RELATORIOS/RELATORIO_2025.csv"
        }

       

# --- Configuração da Página Streamlit ---
st.set_page_config(page_title="Guia Amarela Interativa", page_icon=":scroll:", layout="wide")

# Menu lateral
st.sidebar.title("Navegação")
pagina = st.sidebar.radio(
    "Selecione uma seção:",
    ("🏠 Home", "🏗️ Potencial Construtivo", "📐 Área de Ocupação", "📊 Indicadores Urbanísticos", "🗺️ Mapa Interativo", "🏘️ Análise Estatística de Emissão de Alvarás")
)

# ------------------------------------------------------------------------------ HOME -----------------------------------------------------------------------------------------------

if pagina == "🏠 Home":
        # Estilo customizado CSS 
    st.markdown("""
        <style>
        .titulo-principal {
            background-color: #F9E79F;  /* amarelo pastel */
            padding: 0rem;
            border-radius: 10px;
            font-size: 32px;
            color: #555;
            text-align: center;
            font-weight: bold;
            border: 1px solid #e0e0e0;
        }
        .caixa-cinza {
            background-color: #F2F3F4;
            padding: 1rem;
            border-radius: 10px;
            margin-top: 1rem;
            color: #333;
        }
        .destaque {
            color: #D4AC0D;
            font-weight: bold;
        }
        </style>
    """, unsafe_allow_html=True)
    
    # Título principal
    st.markdown('<div class="titulo-principal">📒 Guia Amarela Interativa</div>', unsafe_allow_html=True)
    
    # Introdução
    st.markdown("""
    <div class="caixa-cinza">
        Esta aplicação tem como objetivo <span class="destaque">modernizar a Consulta Informativa de Lote (CIL)</span>,
        mais conhecida como Guia Amarela, emitida pela Prefeitura de Curitiba.
        <br><br>
        Ao invés de um PDF estático e de difícil interpretação, a proposta aqui é entregar um <span class="destaque">relatório interativo</span>
        com mapas, gráficos, visualizações 3D e explicações acessíveis.
    </div>
    """, unsafe_allow_html=True)
    
    # Funcionalidades principais
    st.markdown("""
    ### 🛠️ Funcionalidades já implementadas
    
    - 📍 **Visualização geográfica** dos lotes com base na Indicação Fiscal.
    - 🧱 **Cálculo e visualização do Potencial Construtivo**, com gráfico 3D interativo.
    - 🧮 **Simulação da Taxa de Ocupação** e área livre construída.
    - 📊 **Análise estatística da emissão de alvarás** por ano e tipologia.
    
    """)
    
    # Rodapé informal
    st.markdown("""
    <br>
    <span style='font-size: 12px; color: gray;'>Desenvolvido como trabalho final da disciplina de Desenvolvimento de Aplicações em Ciências Geodésicas.</span>
    """, unsafe_allow_html=True)

# ---------------------------------------------------------------------------- POTENCIAL CONSTRUTIVO ------------------------------------------------------------------------------------

elif pagina == "🏗️ Potencial Construtivo":
    st.title("Potencial Construtivo")

    st.markdown("Visualize aqui o volume máximo permitidos pelo coeficiente de aproveitamento, altura e recuos mínimos.")

    # Carrega o arquivo GeoJSON localmente
    gdf = gpd.read_file(url_lotes)

    # Caixa de entrada para Indicação Fiscal
    ind_fiscal = st.text_input("Digite a Indicação Fiscal (INDFISCAL):")

    # Verifica se foi digitado algo
    if ind_fiscal:
        lote_filtrado = gdf[gdf["INDFISCAL"] == ind_fiscal]

        if lote_filtrado.empty:
            st.warning("Nenhum lote encontrado com essa indicação fiscal.")
        else:
            lote_geom = lote_filtrado.geometry.values[0]

            # Garantir que seja um Polygon simples
            if lote_geom.is_empty:
                st.error("A geometria do lote está vazia.")
            elif lote_geom.geom_type == "MultiPolygon":
                # Pega o maior polígono do MultiPolygon
                lote_geom = max(lote_geom.geoms, key=lambda a: a.area)

            if lote_geom.geom_type == "Polygon":
                try:
                    x, y = list(lote_geom.exterior.coords.xy[0]), list(lote_geom.exterior.coords.xy[1])
                    area = lote_geom.area
                    ca = st.slider("Coeficiente de Aproveitamento (CA)", 0.5, 4.0, 2.0, 0.1)
                    altura = (ca * area) / (area**0.5)
                    z_base = [0] * len(x)
                    z_top = [altura] * len(x)

                    fig = go.Figure()

                    # base
                    fig.add_trace(go.Scatter3d(x=x, y=y, z=z_base, mode='lines',
                                               line=dict(color='blue', width=4), name='Base'))

                    # topo
                    fig.add_trace(go.Scatter3d(x=x, y=y, z=z_top, mode='lines',
                                               line=dict(color='lightblue', width=4), name='Topo'))

                    # laterais
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

                except Exception as e:
                    st.error(f"Erro ao gerar visualização 3D: {e}")
            else:
                st.error("A geometria selecionada não é um polígono válido.")
    else:
        st.info("Insira a Indicação Fiscal para visualizar o lote.")


# --------------------------------------------------------------------------------------- ÁREA DE OCUPAÇÃO -------------------------------------------------------------------

elif pagina == "📐 Área de Ocupação":
    st.title("Área de Ocupação do Lote")

    st.markdown("Visualize o quanto do lote pode ou não ser ocupado, com base na taxa de ocupação e permeabilidade.")

    # Caixa para buscar o lote
    ind_fiscal_2 = st.text_input("Digite a Indicação Fiscal (INDFISCAL) para simular a ocupação:")

   
    if ind_fiscal_2:
        lote_2 = gdf[gdf["INDFISCAL"] == ind_fiscal_2]

        if lote_2.empty:
            st.warning("Lote não encontrado.")
        else:
            geom = lote_2.geometry.values[0]

            if geom.is_empty:
                st.error("Geometria do lote vazia.")
            elif geom.geom_type == "MultiPolygon":
                geom = max(geom.geoms, key=lambda a: a.area)

            if geom.geom_type == "Polygon":
                try:
                    x, y = list(geom.exterior.coords.xy[0]), list(geom.exterior.coords.xy[1])
                    area_total = geom.area

                    st.markdown(f"**Área total do lote:** {area_total:.2f} m²")

                    # Slider para simular taxa de ocupação
                    ocupacao_pct = st.slider("Taxa de Ocupação (%)", 0, 100, 50, 5)
                    area_ocupada = area_total * (ocupacao_pct / 100)

                    # Suposição de altura mínima para ilustrar
                    altura = 3

                    # Escala proporcional da base do bloco
                    escala = (area_ocupada / area_total) ** 0.5
                    x_centro = sum(x) / len(x)
                    y_centro = sum(y) / len(y)

                    x_scaled = [(xi - x_centro) * escala + x_centro for xi in x]
                    y_scaled = [(yi - y_centro) * escala + y_centro for yi in y]
                    z_base = [0] * len(x)
                    z_top = [altura] * len(x)

                    fig2 = go.Figure()

                    # Geometria original do lote (base)
                    fig2.add_trace(go.Scatter3d(x=x, y=y, z=z_base, mode='lines',
                                                line=dict(color='lightgray', width=3),
                                                name='Área Total'))

                    # Geometria ocupada simulada
                    fig2.add_trace(go.Scatter3d(x=x_scaled, y=y_scaled, z=z_top, mode='lines',
                                                line=dict(color='green', width=4),
                                                name=f'Ocupação ({ocupacao_pct}%)'))

                    # Laterais da ocupação
                    for i in range(len(x)):
                        fig2.add_trace(go.Scatter3d(
                            x=[x_scaled[i], x_scaled[i]], y=[y_scaled[i], y_scaled[i]], z=[0, altura],
                            mode='lines', line=dict(color='green', width=2), showlegend=False
                        ))

                    fig2.update_layout(
                        scene=dict(
                            xaxis_title="X",
                            yaxis_title="Y",
                            zaxis_title="Altura (m)"
                        ),
                        margin=dict(l=0, r=0, b=0, t=30)
                    )

                    st.plotly_chart(fig2, use_container_width=True)
                    
                    # Gráfico de pizza da ocupação
                    ocupacao_labels = ['Área Ocupada', 'Área Livre']
                    ocupacao_values = [area_ocupada, area_total - area_ocupada]
                    ocupacao_colors = ['green', 'lightgray']

                    fig_pizza = go.Figure(data=[go.Pie(
                        labels=ocupacao_labels,
                        values=ocupacao_values,
                        marker=dict(colors=ocupacao_colors),
                        hole=0.4
                        )])

                    fig_pizza.update_layout(
                        title="Distribuição da Ocupação no Lote",
                        margin=dict(l=0, r=0, t=30, b=0),
                        height=400
                    )

                    st.plotly_chart(fig_pizza, use_container_width=True)
                    st.markdown(f"**Área ocupada:** {area_ocupada:.2f} m²")

                except Exception as e:
                    st.error(f"Erro ao gerar visualização: {e}")
            else:
                st.error("Geometria não é um polígono.")
   
# --------------------------------------------------------------------- INDICADORES -------------------------------------------------------------

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

# ---------------------------------------------------------------- MAPA INTERATIVO ----------------------------------------------------------------------------

elif pagina == "🗺️ Mapa Interativo":
    st.title("Mapa Interativo")

        # --- Criação do Mapa Base Folium ---
    m = folium.Map(location=[-25.42, -49.25], zoom_start=13, tiles="CartoDB positron")

    # Adiciona a camada GeoJSON
    campos_seguro = ["CDLOTE", "INDFISCAL", "CDVIA", "NMVIA"]  

    folium.GeoJson(
        gdf_lotes,
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

#---------------------------------------------------------- ANÁLISE ESTATÍSTICA --------------------------------------------------------------

elif pagina == "🏘️ Análise Estatística de Emissão de Alvarás":
    st.title("🏘️ Análise Estatística de Emissão de Alvarás")

    # Seleção do ano pelo usuário
    ano_selecionado = st.selectbox("Selecione o ano do relatório", list(urls_alvaras.keys()))
    url_csv = urls_alvaras[ano_selecionado]

    # Carregamento dos dados de alvarás
    try:
        df_alvaras = pd.read_csv(url_csv, sep=';')
        st.success(f"Relatório de alvarás de {ano_selecionado} carregado com sucesso.")
    except Exception as e:
        st.error(f"Erro ao carregar os dados do relatório: {e}")
        st.stop()

    # Verifica se a coluna INDFISCAL existe no gdf_lotes
    col_fiscal_lotes = None
    for col in gdf_lotes.columns:
        if 'fiscal' in col.lower():
            col_fiscal_lotes = col
            break

    if col_fiscal_lotes:
        # Padroniza a coluna
        gdf_lotes.rename(columns={col_fiscal_lotes: 'INDFISCAL'}, inplace=True)
        gdf_lotes['INDFISCAL'] = gdf_lotes['INDFISCAL'].astype(str)
        df_alvaras['INDFISCAL'] = df_alvaras['INDFISCAL'].astype(str)
        df_alvaras['INDFISCAL'] = df_alvaras['INDFISCAL'].str.replace('.', '', regex=False)

           # Cruzamento entre alvarás e lotes
    gdf_alvaras_lotes = gdf_lotes.merge(df_alvaras, on='INDFISCAL', how='inner')
    
    # Verifica interseção de INDFISCAL
    indfiscal_lotes = set(gdf_lotes['INDFISCAL'].unique())
    indfiscal_alvaras = set(df_alvaras['INDFISCAL'].unique())
    interseccao = indfiscal_lotes.intersection(indfiscal_alvaras)
    
    st.write(f"🔍 Foram encontradas {len(interseccao)} indicações fiscais em comum entre alvarás e lotes.")
    
    num_cruzamentos = len(gdf_alvaras_lotes)
    if num_cruzamentos > 0:
        st.success(f"✅ Foram encontrados {num_cruzamentos} cruzamentos entre lotes e alvarás.")
    else:
        st.warning("⚠️ Nenhum cruzamento entre lotes e alvarás foi encontrado.")
    
    # Visualização no mapa, se houver cruzamentos
    if num_cruzamentos > 0 and 'Uso(s) Alvará' in gdf_alvaras_lotes.columns:
        st.markdown("### 🗺️ Visualização dos Lotes com Alvarás Emitidos por Uso")
    
        m_alvaras = folium.Map(location=[-25.42, -49.25], zoom_start=13, tiles='CartoDB positron')
    
        # Cores por uso
        usos = gdf_alvaras_lotes['Uso(s) Alvará'].unique()
        cores = px.colors.qualitative.Safe
        cores_dict = {uso: cores[i % len(cores)] for i, uso in enumerate(usos)}
    
        # Adiciona todos os lotes ao mapa de uma vez, com estilos por uso
        folium.GeoJson(
            gdf_alvaras_lotes,
            name="Lotes com Alvará",
            tooltip=folium.GeoJsonTooltip(
                fields=["INDFISCAL", "Uso(s) Alvará"],
                aliases=["Indicação Fiscal", "Uso"],
                sticky=True
            ),
            style_function=lambda feature: {
                "fillColor": cores_dict.get(feature["properties"]["Uso(s) Alvará"], "gray"),
                "color": "black",
                "weight": 1,
                "fillOpacity": 0.5
            }
        ).add_to(m_alvaras)
                               
        folium.LayerControl().add_to(m_alvaras)
        st_folium(m_alvaras, width="100%", height=700)
   
    elif num_cruzamentos > 0:
        st.warning("⚠️ A coluna 'Uso(s) Alvará' não foi encontrada nos dados cruzados.")

        # Verifica se a coluna com INDFISCAL está presente
    if 'INDFISCAL' in gdf_lotes.columns:
    
        # Verifica se o campo 'Uso(s) Alvará' existe
        if 'Uso(s) Alvará' in df_alvaras.columns:
    
            # Gráfico de barras com distribuição por uso
            st.subheader("📊 Distribuição de Alvarás por Uso")
            uso_counts = df_alvaras['Uso(s) Alvará'].value_counts().reset_index()
            uso_counts.columns = ['Uso(s) Alvará', 'QUANTIDADE']
    
            fig = px.bar(
                uso_counts,
                x='Uso(s) Alvará',
                y='QUANTIDADE',
                title=f'Alvarás emitidos por uso - {ano_selecionado}',
                labels={'Uso(s) Alvará': 'Tipologia Construtiva', 'QUANTIDADE': 'Quantidade'},
                color='Uso(s) Alvará',
                color_discrete_map=cores_dict
            )
    
            st.plotly_chart(fig, use_container_width=True)
    
        else:
            st.info("ℹ️ O campo 'Uso(s) Alvará' não está presente no relatório.")
    
    else:
        st.error("❌ A coluna com a indicação fiscal não foi encontrada no GeoDataFrame dos lotes.")
