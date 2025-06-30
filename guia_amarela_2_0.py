import streamlit as st
from streamlit_folium import st_folium
import folium
import geopandas as gpd
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


#URLs
url_lotes = "https://raw.githubusercontent.com/BryanSprenger/Trabalho-Final/main/Lotes2021_6.geojson"
url_zonas_geojson = "https://raw.githubusercontent.com/BryanSprenger/Trabalho-Final/refs/heads/main/ZONEAMENTO.geojson"
url_indicadores_csv = "https://raw.githubusercontent.com/BryanSprenger/Trabalho-Final/refs/heads/main/ZONEAMENTO_USOS_COEFICIENTES.csv"

#GDFs
gdf_lotes = gpd.read_file(url_lotes)
gdf_lotes = gdf_lotes[gdf_lotes.is_valid & ~gdf_lotes.geometry.is_empty]
gdf_zonas = gpd.read_file(url_zonas_geojson)
gdf_zonas = gdf_zonas.set_geometry("geometry")  # caso necessário

df_zoneamento_indices = pd.read_csv(url_indicadores_csv, sep=",")

    
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
            padding: 2rem;
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
    st.title("🏗️ Potencial Construtivo do Lote")
    st.markdown("Visualize aqui o volume máximo permitido pelo coeficiente de aproveitamento, altura e recuos mínimos.")

    # Entrada da INDFISCAL
    ind_fiscal = st.text_input("Digite a Indicação Fiscal (INDFISCAL):")
   
    if ind_fiscal:
        gdf_lotes["INDFISCAL"] = gdf_lotes["INDFISCAL"].astype(str)
        ind_fiscal = str(ind_fiscal).strip()

        lote_selecionado = gdf_lotes[gdf_lotes["INDFISCAL"] == ind_fiscal]

        if lote_selecionado.empty:
            st.warning("⚠️ Nenhum lote encontrado com essa Indicação Fiscal.")
        else:
            # Exibir área do lote
            area_m2 = lote_selecionado.geometry.area.iloc[0]
            st.success(f"✅ Área do lote: **{area_m2:.2f} m²**")

            geom_lote = lote_selecionado.geometry.values[0]

            if geom_lote.is_empty:
                st.error("A geometria do lote está vazia.")
            elif geom_lote.geom_type == "MultiPolygon":
                geom_lote = max(geom_lote.geoms, key=lambda a: a.area)

            # Interseção com zona
            try:
                zona_intersectada = gdf_zonas[gdf_zonas.intersects(geom_lote)]

                if not zona_intersectada.empty:
                    zona_nome = zona_intersectada.iloc[0]["NM_ZONA"]

                    # Busca o CA correspondente
                    zona_match = df_zoneamento_indices[df_zoneamento_indices["ZONA"] == zona_nome]

                    if not zona_match.empty:
                        ca_max = float(zona_match["CA_MAXIMO"].values[0])
                        st.info(f"🏙️ Zona: **{zona_nome}** — CA Máximo: **{ca_max}**")

                        # Slider de simulação
                        ca = st.slider("Coeficiente de Aproveitamento (CA)", 0.1, ca_max, min(1.0, ca_max), 0.1)

                        altura = (ca * area_m2) / (area_m2 ** 0.5)

                        x, y = list(geom_lote.exterior.coords.xy[0]), list(geom_lote.exterior.coords.xy[1])
                        z_base = [0] * len(x)
                        z_top = [altura] * len(x)

                        fig = go.Figure()

                        # Base
                        fig.add_trace(go.Scatter3d(x=x, y=y, z=z_base, mode='lines',
                                                   line=dict(color='blue', width=4), name='Base'))

                        # Topo
                        fig.add_trace(go.Scatter3d(x=x, y=y, z=z_top, mode='lines',
                                                   line=dict(color='lightblue', width=4), name='Topo'))

                        # Laterais
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
                        st.warning("⚠️ Zona identificada no mapa, mas não localizada na tabela de índices.")
                else:
                    st.warning("⚠️ A zona correspondente ao lote não foi identificada no mapa.")
            except Exception as e:
                st.error(f"Erro ao processar zona e CA: {e}")
    else:
        st.info("Digite uma Indicação Fiscal para iniciar.")

# --------------------------------------------------------------------------------------- ÁREA DE OCUPAÇÃO -------------------------------------------------------------------

elif pagina == "📐 Área de Ocupação":
    st.title("📐 Área de Ocupação do Lote")
    st.markdown("Visualize o quanto do lote pode ser ocupado com base na taxa de ocupação da zona urbanística correspondente.")

    # Entrada da Indicação Fiscal
    ind_fiscal_2 = st.text_input("Digite a Indicação Fiscal (INDFISCAL) para simular a ocupação:")

    if ind_fiscal_2:
        gdf_lotes['INDFISCAL'] = gdf_lotes['INDFISCAL'].astype(str)
        ind_fiscal_2 = ind_fiscal_2.strip()

        lote_2 = gdf_lotes[gdf_lotes["INDFISCAL"] == ind_fiscal_2]

        if lote_2.empty:
            st.warning("⚠️ Lote não encontrado.")
        else:
            geom = lote_2.geometry.values[0]

            if geom.is_empty:
                st.error("⚠️ Geometria do lote vazia.")
            elif geom.geom_type == "MultiPolygon":
                geom = max(geom.geoms, key=lambda a: a.area)

            if geom.geom_type == "Polygon":
                try:
                    x, y = list(geom.exterior.coords.xy[0]), list(geom.exterior.coords.xy[1])
                    area_total = geom.area
                    st.markdown(f"**📏 Área total do lote:** {area_total:.2f} m²")

                    # Interseção com zoneamento
                    zona_intersectada = gdf_zonas[gdf_zonas.intersects(geom)]

                    if not zona_intersectada.empty:
                        zona_nome = zona_intersectada.iloc[0]["NM_ZONA"]
                        zona_match = df_zoneamento_indices[df_zoneamento_indices["ZONA"] == zona_nome]

                        if not zona_match.empty:
                            taxa_maxima = float(zona_match["TAXA_OCUPACAO_MAX"].values[0])
                            st.info(f"🏙️ Zona: **{zona_nome}** — Taxa Máxima de Ocupação: **{taxa_maxima:.1f}%**")

                            ocupacao_pct = st.slider("Taxa de Ocupação (%)", 0, int(taxa_maxima), int(taxa_maxima // 2), 5)
                            area_ocupada = area_total * (ocupacao_pct / 100)
                            altura = 3  # altura simbólica

                            # Escala do bloco de ocupação
                            escala = (area_ocupada / area_total) ** 0.5
                            x_centro = sum(x) / len(x)
                            y_centro = sum(y) / len(y)

                            x_scaled = [(xi - x_centro) * escala + x_centro for xi in x]
                            y_scaled = [(yi - y_centro) * escala + y_centro for yi in y]
                            z_base = [0] * len(x)
                            z_top = [altura] * len(x)

                            fig2 = go.Figure()

                            # Lote original
                            fig2.add_trace(go.Scatter3d(x=x, y=y, z=z_base, mode='lines',
                                                        line=dict(color='lightgray', width=3),
                                                        name='Área Total'))

                            # Ocupação simulada
                            fig2.add_trace(go.Scatter3d(x=x_scaled, y=y_scaled, z=z_top, mode='lines',
                                                        line=dict(color='green', width=4),
                                                        name=f'Ocupação ({ocupacao_pct}%)'))

                            for i in range(len(x)):
                                fig2.add_trace(go.Scatter3d(
                                    x=[x_scaled[i], x_scaled[i]],
                                    y=[y_scaled[i], y_scaled[i]],
                                    z=[0, altura],
                                    mode='lines',
                                    line=dict(color='green', width=2),
                                    showlegend=False
                                ))

                            fig2.update_layout(
                                scene=dict(
                                    xaxis_title="X",
                                    yaxis_title="Y",
                                    zaxis_title="Altura (m)"
                                ),
                                margin=dict(l=0, r=0, t=30, b=0)
                            )

                            st.plotly_chart(fig2, use_container_width=True)

                            # Gráfico de pizza
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
                            st.markdown(f"📌 **Área ocupada simulada:** {area_ocupada:.2f} m²")

                        else:
                            st.warning("⚠️ Zona identificada no mapa, mas não encontrada na tabela de índices.")
                    else:
                        st.warning("⚠️ Zona do lote não foi identificada.")
                except Exception as e:
                    st.error(f"Erro ao gerar visualização: {e}")
            else:
                st.error("⚠️ Geometria não é um polígono válido.")
    else:
        st.info("Insira a Indicação Fiscal para simular a ocupação do lote.")
   
# --------------------------------------------------------------------- INDICADORES -------------------------------------------------------------

elif pagina == "📊 Indicadores Urbanísticos":
    st.title("📊 Indicadores Urbanísticos do Lote")
    st.markdown("Insira a Indicação Fiscal para consultar os índices urbanísticos aplicáveis ao lote, como coeficiente de aproveitamento, usos permitidos e permissíveis.")

    # URLs dos dados
    url_zoneamento_csv = "https://raw.githubusercontent.com/BryanSprenger/Trabalho-Final/refs/heads/main/ZONEAMENTO_USOS_COEFICIENTES.csv"
    url_zoneamento_geojson = "https://raw.githubusercontent.com/BryanSprenger/Trabalho-Final/refs/heads/main/ZONEAMENTO.geojson"

    try:
        # Carrega os dados
        df_indicadores = pd.read_csv(url_zoneamento_csv, sep=',')
        gdf_zonas = gpd.read_file(url_zoneamento_geojson)
        gdf_lotes = gpd.read_file(url_lotes)

        # Padronização
        df_indicadores.columns = df_indicadores.columns.str.upper().str.strip()
        gdf_zonas.columns = gdf_zonas.columns.str.upper().str.strip()
        gdf_zonas = gdf_zonas.set_geometry("GEOMETRY")
        gdf_lotes['INDFISCAL'] = gdf_lotes['INDFISCAL'].astype(str)

        # Entrada do usuário
        indfiscal_zona = st.text_input("Digite a Indicação Fiscal (INDFISCAL):")

        if indfiscal_zona:
            indfiscal_zona = str(indfiscal_zona).strip()
            lote_selecionado = gdf_lotes[gdf_lotes["INDFISCAL"] == indfiscal_zona]

            if lote_selecionado.empty:
                st.warning("⚠️ Nenhum lote encontrado com essa indicação fiscal.")
            else:
                geom_lote = lote_selecionado.geometry.values[0]
                if geom_lote.geom_type == "MultiPolygon":
                    geom_lote = max(geom_lote.geoms, key=lambda a: a.area)

                zona_intersectada = gdf_zonas[gdf_zonas.geometry.intersects(geom_lote)]

                if not zona_intersectada.empty:
                    zona_lote = zona_intersectada.iloc[0]['NM_ZONA']
                    zona_lote = str(zona_lote).strip().upper()
                    st.success(f"📌 Zona identificada no mapa: `{zona_lote}`")

                    zona_info = df_indicadores[df_indicadores['ZONA'] == zona_lote]

                    if not zona_info.empty:
                        st.markdown("### 📋 Tabela de Indicadores Urbanísticos")

                        colunas_renomeadas = {
                            "ZONA": "Zona",
                            "CA_BASICO": "CA Básico",
                            "CA_MAXIMO": "CA Máximo",
                            "TAXA_OCUPACAO_MAX": "Taxa de Ocupação (%)",
                            "TAXA_PERMEABILIDADE_MIN": "Taxa de Permeabilidade (%)",
                            "USOS_PERMITIDOS": "Usos Permitidos",
                            "USOS_PERMISSIVEIS": "Usos Permissíveis"
                        }
                        zona_info = zona_info.rename(columns=colunas_renomeadas)

                        for col in ["CA Básico", "CA Máximo", "Taxa de Ocupação (%)", "Taxa de Permeabilidade (%)"]:
                            if col in zona_info.columns:
                                zona_info[col] = zona_info[col].astype(float).round(2)

                        # Calcula área do lote
                        area_lote = lote_selecionado.geometry.area.iloc[0]

                        ca_basico_m2 = round(area_lote * zona_info["CA Básico"].values[0], 2)
                        ca_maximo_m2 = round(area_lote * zona_info["CA Máximo"].values[0], 2)
                        ocupacao_m2 = round(area_lote * zona_info["Taxa de Ocupação (%)"].values[0] / 100, 2)
                        permeabilidade_m2 = round(area_lote * zona_info["Taxa de Permeabilidade (%)"].values[0] / 100, 2)

                        # Cria DataFrame com valores calculados
                        linha_m2 = pd.DataFrame({
                            "Zona": ["(equivalente em m²)"],
                            "CA Básico": [ca_basico_m2],
                            "CA Máximo": [ca_maximo_m2],
                            "Taxa de Ocupação (%)": [ocupacao_m2],
                            "Taxa de Permeabilidade (%)": [permeabilidade_m2],
                            "Usos Permitidos": ["—"],
                            "Usos Permissíveis": ["—"]
                        })

                        # Junta original + linha m²
                        tabela_final = pd.concat([zona_info, linha_m2], ignore_index=True)

                        st.dataframe(tabela_final, use_container_width=True)

                        # Lista os usos
                        if "Usos Permitidos" in zona_info.columns:
                            usos_permitidos_raw = zona_info["Usos Permitidos"].values[0]
                            if isinstance(usos_permitidos_raw, str) and usos_permitidos_raw.strip():
                                usos_permitidos = [uso.strip() for uso in usos_permitidos_raw.split(";") if uso.strip()]
                                st.markdown("#### ✅ Usos Permitidos")
                                for uso in usos_permitidos:
                                    st.markdown(f"- {uso}")
                            else:
                                st.info("ℹ️ Nenhum uso permitido especificado.")
                        
                        if "Usos Permissíveis" in zona_info.columns:
                            usos_permissiveis_raw = zona_info["Usos Permissíveis"].values[0]
                            if isinstance(usos_permissiveis_raw, str) and usos_permissiveis_raw.strip():
                                usos_permissiveis = [uso.strip() for uso in usos_permissiveis_raw.split(";") if uso.strip()]
                                st.markdown("#### ⚠️ Usos Permissíveis")
                                for uso in usos_permissiveis:
                                    st.markdown(f"- {uso}")
                            else:
                                st.info("ℹ️ Nenhum uso permissível especificado.")

                        if "Usos Permissíveis" in zona_info.columns:
                            usos_permissiveis_raw = zona_info["Usos Permissíveis"].values[0]
                            if isinstance(usos_permissiveis_raw, str) and usos_permissiveis_raw.strip():
                                usos_permissiveis = [uso.strip() for uso in usos_permissiveis_raw.split(";") if uso.strip()]
                                st.markdown("#### ⚠️ Usos Permissíveis")
                                for uso in usos_permissiveis:
                                    st.markdown(f"- {uso}")
                            else:
                                st.info("ℹ️ Nenhum uso permissível especificado.")
                                    else:
                                        st.warning("⚠️ Zona identificada no mapa, mas não localizada na tabela de indicadores.")
                else:
                    st.warning("⚠️ O lote não intercepta nenhuma zona urbanística.")
    except Exception as e:
        st.error(f"Erro ao carregar dados de zoneamento: {e}")

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
