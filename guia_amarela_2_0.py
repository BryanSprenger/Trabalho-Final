import streamlit as st
from streamlit_folium import st_folium
import folium
import geopandas as gpd
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from folium.plugins import Fullscreen, MeasureControl, MiniMap


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
    
    - 🗺️ **Visualização geográfica** dos lotes com base na Indicação Fiscal.
    - 🏗️ **Cálculo e visualização do Potencial Construtivo**, com gráfico 3D interativo.
    - 📐 **Simulação da Taxa de Ocupação** e área livre construída.
    - 📊 **Indicadores Urbanisticos** com base no zoneamento do lote 
    - 🏘️ **Análise estatística da emissão de alvarás** por ano e tipologia.
    
    """)
    
    # Rodapé informal
    st.markdown(
        """
        <div style="background-color: #f8f9fa; padding: 20px; border-radius: 10px; margin-top: 30px;">
            <p style="font-size: 14px; color: #555;">
            <strong>📚 Este Projeto foi desenvolvido como trabalho final da disciplina de <em>Desenvolvimento de Aplicações Geoespaciais</em><br>
            da Pós-Graduação em Ciências Geodésicas da UFPR.</strong><br><br>
            <strong>👨‍🎓 Discente:</strong> Bryan Leonardo Franco Sprenger<br>
            <strong>📅 Ano:</strong> 2025
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

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

        # Corrige colunas e geometrias
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

                    zona_info = df_indicadores[df_indicadores['ZONA'].str.upper().str.strip() == zona_lote]

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
                                zona_info[col] = pd.to_numeric(zona_info[col], errors='coerce').round(1)

                        colunas_tabela = ["Zona", "CA Básico", "CA Máximo", "Taxa de Ocupação (%)", "Taxa de Permeabilidade (%)"]
                        st.dataframe(zona_info[colunas_tabela], use_container_width=True)

                        # Cálculos com base na área do lote
                        area_lote = geom_lote.area
                        st.markdown("### 📐 Cálculo Aplicado ao Lote")
                        ca_basico = zona_info["CA Básico"].values[0]
                        ca_maximo = zona_info["CA Máximo"].values[0]
                        taxa_ocupacao = zona_info["Taxa de Ocupação (%)"].values[0]
                        taxa_permeavel = zona_info["Taxa de Permeabilidade (%)"].values[0]

                        st.markdown(f"- **Área do Lote:** `{area_lote:.2f} m²`")
                        st.markdown(f"- **CA Básico (m²):** `{(ca_basico * area_lote):.2f} m²`")
                        st.markdown(f"- **CA Máximo (m²):** `{(ca_maximo * area_lote):.2f} m²`")
                        st.markdown(f"- **Área Ocupável Máxima:** `{(taxa_ocupacao / 100 * area_lote):.2f} m²`")
                        st.markdown(f"- **Área Permeável Mínima:** `{(taxa_permeavel / 100 * area_lote):.2f} m²`")

                        # Usos Permitidos
                        if "Usos Permitidos" in zona_info.columns:
                            usos_permitidos_raw = zona_info["Usos Permitidos"].values[0]
                            if isinstance(usos_permitidos_raw, str) and usos_permitidos_raw.strip():
                                usos_permitidos = [uso.strip() for uso in usos_permitidos_raw.split(";") if uso.strip()]
                                st.markdown("#### ✅ Usos Permitidos")
                                for uso in usos_permitidos:
                                    st.markdown(f"- {uso}")
                            else:
                                st.info("ℹ️ Nenhum uso permitido especificado.")

                        # Usos Permissíveis
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
    st.title("🗺️ Mapa Interativo")
    st.markdown("Visualize os lotes e consulte informações básicas com base na indicação fiscal (IF).")

    # Entrada do usuário para buscar lote
    ind_fiscal_map = st.text_input("🔎 Digite a Indicação Fiscal para localizar no mapa:")

    # Garante tipo string
    gdf_lotes['INDFISCAL'] = gdf_lotes['INDFISCAL'].astype(str)

    # Se foi digitada uma IF válida, filtra e pega centroide
    if ind_fiscal_map:
        ind_fiscal_map = ind_fiscal_map.strip()
        lote_localizado = gdf_lotes[gdf_lotes['INDFISCAL'] == ind_fiscal_map]

        if not lote_localizado.empty:
            centroid = lote_localizado.geometry.iloc[0].centroid
            lat, lon = centroid.y, centroid.x
            zoom = 18
            st.success(f"Lote localizado. Mapa centralizado na IF: `{ind_fiscal_map}`")
        else:
            st.warning("❌ Nenhum lote encontrado com essa Indicação Fiscal.")
            lat, lon, zoom = -25.42, -49.25, 13
    else:
        lat, lon, zoom = -25.42, -49.25, 13

    # Criação do Mapa
    m = folium.Map(location=[lat, lon], zoom_start=zoom, tiles="CartoDB positron", control_scale=True)

    # Campos seguros para mostrar no tooltip
    campos_seguro = ["CDLOTE", "INDFISCAL", "CDVIA", "NMVIA"]

    # Adiciona GeoJSON dos lotes
    folium.GeoJson(
        gdf_lotes,
        name="Lotes",
        tooltip=folium.GeoJsonTooltip(
            fields=campos_seguro,
            aliases=["Código do Lote", "Indicação Fiscal", "Código da Via", "Nome da Via"],
            sticky=True
        )
    ).add_to(m)

    folium.LayerControl().add_to(m)

    # Exibe o mapa no Streamlit
    st_data = st_folium(m, width="100%", height=700)

    # Exibe informações da IF abaixo
    if ind_fiscal_map and not lote_localizado.empty:
        st.markdown("### 📋 Informações do Lote")
        info_lote = lote_localizado[["INDFISCAL", "CDLOTE", "CDVIA", "NMVIA"]].rename(columns={
            "INDFISCAL": "Indicação Fiscal",
            "CDLOTE": "Código do Lote",
            "CDVIA": "Código da Via",
            "NMVIA": "Nome da Via"
        })
        st.dataframe(info_lote.reset_index(drop=True), use_container_width=True)


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


#---------------------------------------------------------- ESTUDO DE VIABILIDADE --------------------------------------------------------------

# --- Funções de Carregamento e Pré-processamento de Dados (Cacheada) ---
@st.cache_data
def load_and_preprocess_data():
    """
    Carrega e pré-processa todos os dados (alvarás, lotes, zoneamento)
    e calcula as features necessárias.
    Esta função será executada apenas uma vez graças ao st.cache_data.
    """
    st.write("Carregando e pré-processando dados... Isso pode levar alguns minutos.")

    # --- SEÇÃO 1: Carregamento e Pré-processamento dos Dados de Alvarás ---
    urls_alvaras = {
        str(ano): f"https://raw.githubusercontent.com/BryanSprenger/Trabalho-Final/refs/heads/main/RELATORIOS/RELATORIO_{ano}.csv"
        for ano in range(2000, 2025)
    }

    alvaras_dfs = []
    for ano, url in urls_alvaras.items():
        try:
            df = pd.read_csv(url, sep=';', encoding='utf-8')
            df.columns = df.columns.str.strip().str.lower()

            df.rename(columns={
                'indfiscal': 'INDFISCAL',
                'área construída': 'area_construida',
                'metragem construída lote': 'area_construida',
                'uso(s) alvará': 'tipologia_construcao_alvara',
                'quantidade pavimentos': 'num_pavimentos_projeto_alvara'
            }, inplace=True, errors='ignore')

            if 'tipologia_construcao_alvara' in df.columns:
                df['tipologia_construcao_alvara'] = df['tipologia_construcao_alvara'].astype(str).str.strip().str.upper()

            cols_to_keep_alvaras = ['INDFISCAL', 'area_construida']
            if 'INDFISCAL' in df.columns and 'area_construida' in df.columns:
                alvaras_dfs.append(df[cols_to_keep_alvaras])
            
        except Exception as e:
            st.warning(f"Erro ao carregar alvará de {ano}: {e}")

    alvaras_df = pd.concat(alvaras_dfs, ignore_index=True)
    st.write(f"Total de registros de alvarás carregados: {len(alvaras_df)}")

    alvaras_agregados_lote = alvaras_df.groupby('INDFISCAL').agg(
        area_construida_existente=('area_construida', 'sum')
    ).reset_index()


    # --- SEÇÃO 2: Carregamento e Pré-processamento dos Dados Espaciais e de Zoneamento ---
    url_zoneamento_geojson = "https://raw.githubusercontent.com/BryanSprenger/Trabalho-Final/refs/heads/main/ZONEAMENTO.geojson"
    url_lotes = "https://raw.githubusercontent.com/BryanSprenger/Trabalho-Final/main/Lotes2021_6.geojson"
    url_zoneamento_csv = "https://raw.githubusercontent.com/BryanSprenger/Trabalho-Final/refs/heads/main/ZONEAMENTO_USOS_COEFICIENTES.csv"

    gdf_lotes = gpd.read_file(url_lotes)

    geometry_col_name_found = None
    for col in gdf_lotes.columns:
        if str(gdf_lotes[col].dtype).startswith('geometry'):
            geometry_col_name_found = col
            break

    if geometry_col_name_found:
        gdf_lotes = gdf_lotes.set_geometry(geometry_col_name_found)
        if gdf_lotes.geometry.empty or not hasattr(gdf_lotes.geometry.iloc[0], "geom_type"):
            st.error(f"A coluna de geometria '{geometry_col_name_found}' existe, mas não contém objetos geométricos válidos (shapely) ou está vazia.")
            st.stop()
    else:
        st.error("Nenhuma coluna do tipo 'geometry' foi encontrada no GeoDataFrame dos lotes.")
        st.stop()

    new_columns = []
    for col in gdf_lotes.columns:
        if col == gdf_lotes.geometry.name:
            new_columns.append(col)
        else:
            new_columns.append(col.strip().upper())
    gdf_lotes.columns = new_columns

    gdf_lotes.rename(columns={'INDFISCAL': 'INDFISCAL'}, inplace=True, errors='ignore')
    gdf_lotes["AREA_TOTAL"] = gdf_lotes.geometry.area

    df_zoneamento_info = pd.read_csv(url_zoneamento_csv, encoding='utf-8-sig')
    df_zoneamento_info.columns = df_zoneamento_info.columns.str.strip().str.upper()

    substituicoes = {
        "LIVRE": 6.0,
        "ONEROSO_CONFORME_QUADRO": 6.0, "ONEROSO": 6.0, "SEM LIMITE": 6.0,
        "-": 0.0001, "": 0.0001, "N/A": 0.0001,
        "VER_LEI_ESPECIFICA": 0.0001, "VER_QUADROS_ESPECIFICOS": 0.0001,
        "VER_SUBZONA": 0.0001, "VER_SUBSETOR": 0.0001, "VER_ZONA_ATRAVESSADA": 0.0001,
        "VER_PDR": 0.0001, "VARIA_POR_VIA": 0.0001, "LEGISLAÇÃO_ESPECÍFICA": 0.0001,
    }
    df_zoneamento_info["CA_MAXIMO"] = (
        df_zoneamento_info["CA_MAXIMO"].astype(str).str.upper().replace(substituicoes, regex=False).str.replace(",", ".", regex=False)
    )
    df_zoneamento_info["CA_MAXIMO"] = pd.to_numeric(df_zoneamento_info["CA_MAXIMO"], errors='coerce').fillna(0.0001)

    gdf_zoneamento_temp = gpd.read_file(url_zoneamento_geojson)
    zoneamento_temp_new_cols = []
    for col in gdf_zoneamento_temp.columns:
        if col == gdf_zoneamento_temp.geometry.name:
            zoneamento_temp_new_cols.append(col)
        else:
            zoneamento_temp_new_cols.append(col.strip().upper())
    gdf_zoneamento_temp.columns = zoneamento_temp_new_cols

    gdf_zoneamento_temp.rename(columns={'NM_ZONA': 'ZONA'}, inplace=True, errors='ignore')
    gdf_zoneamento_temp.rename(columns={'ZONA_DESCRICAO': 'ZONA'}, inplace=True, errors='ignore')

    if gdf_zoneamento_temp.geometry.name != 'geometry':
        if 'GEOMETRY' in gdf_zoneamento_temp.columns:
            gdf_zoneamento_temp.rename(columns={'GEOMETRY': 'geometry'}, inplace=True)
        gdf_zoneamento_temp = gdf_zoneamento_temp.set_geometry('geometry')

    gdf_lotes_com_zona = gpd.sjoin(gdf_lotes, gdf_zoneamento_temp[['geometry', 'ZONA']], how="left", predicate="within")

    if 'index_left' in gdf_lotes_com_zona.columns:
        gdf_lotes_com_zona.drop(columns=['index_left'], inplace=True)
    if 'index_right' in gdf_lotes_com_zona.columns:
        gdf_lotes_com_zona.drop(columns=['index_right'], inplace=True)

    gdf_lotes_com_zona = gdf_lotes_com_zona.drop_duplicates(subset=['INDFISCAL'])
    gdf_lotes = gdf_lotes_com_zona.copy()

    if 'NM_ZONA' in gdf_lotes.columns:
        gdf_lotes.rename(columns={'NM_ZONA': 'ZONA'}, inplace=True)
    elif 'ZONA_DESCRICAO' in gdf_lotes.columns:
        gdf_lotes.rename(columns={'ZONA_DESCRICAO': 'ZONA'}, inplace=True)

    gdf_lotes = gdf_lotes.merge(
        df_zoneamento_info[['ZONA', 'CA_BASICO', 'CA_MAXIMO', 'USOS_PERMITIDOS', 'USOS_PERMISSIVEIS', 'TAXA_OCUPACAO_MAX', 'TAXA_PERMEABILIDADE_MIN']],
        left_on='ZONA',
        right_on='ZONA',
        how='left'
    )

    gdf_lotes.rename(columns={
        'CA_MAXIMO': 'CA_MAX',
        'USOS_PERMITIDOS': 'USOS_PERMITIDOS_ZONA_STRING',
        'USOS_PERMISSIVEIS': 'USOS_PERMISSIVEIS_ZONA_STRING'
    }, inplace=True)

    gdf_lotes['CA_MAX'] = gdf_lotes['CA_MAX'].fillna(0.0001)
    gdf_lotes['TAXA_OCUPACAO_MAX'] = pd.to_numeric(gdf_lotes['TAXA_OCUPACAO_MAX'], errors='coerce').fillna(0.0)
    gdf_lotes['TAXA_PERMEABILIDADE_MIN'] = pd.to_numeric(gdf_lotes['TAXA_PERMEABILIDADE_MIN'], errors='coerce').fillna(0.0)


    # --- EXPLODIR USOS E POPULAR all_unique_uses AQUI ---
    # Função auxiliar para processar e coletar usos
    def process_uses_and_collect_internal(use_string): # Renomeada para evitar conflito de escopo
        if not isinstance(use_string, str) or not use_string.strip():
            return []
        uses = [u.strip().upper() for u in use_string.split(';') if u.strip()]
        global all_unique_uses # Acessa a variável global
        all_unique_uses.update(uses)
        return uses

    gdf_lotes['LISTA_USOS_PERMITIDOS'] = gdf_lotes['USOS_PERMITIDOS_ZONA_STRING'].apply(process_uses_and_collect_internal)
    
    # --- Merge dos alvarás agregados com gdf_lotes ---
    gdf_lotes = gdf_lotes.merge(alvaras_agregados_lote, on="INDFISCAL", how="left")
    gdf_lotes["area_construida_existente"] = gdf_lotes["area_construida_existente"].fillna(0)

    # Calcular CA_REAL e AREA_DISPONIVEL
    gdf_lotes["CA_REAL"] = np.where(
        gdf_lotes["AREA_TOTAL"] > 0,
        gdf_lotes["area_construida_existente"] / gdf_lotes["AREA_TOTAL"],
        0
    )
    gdf_lotes["AREA_DISPONIVEL"] = gdf_lotes["AREA_TOTAL"] - gdf_lotes["area_construida_existente"]

    # --- SEÇÃO 4: Cálculo de Informações dos Vizinhos ---
    def calcular_vizinhos_info_otimizado_internal(gdf_input, buffer_dist=50): # Renomeada para evitar conflito
        gdf_copy = gdf_input.copy() # Trabalha em uma cópia para evitar SettingWithCopyWarning
        if 'INDFISCAL' not in gdf_copy.columns:
            st.error("A coluna 'INDFISCAL' não foi encontrada para calcular vizinhos.")
            st.stop()
        if gdf_copy.geometry.name is None:
            st.error("A coluna de geometria não está definida para o GeoDataFrame de vizinhos.")
            st.stop()
        
        gdf_copy['buffer_geometry'] = gdf_copy.geometry.buffer(buffer_dist)

        sjoin_result = gpd.sjoin(
            gdf_copy.set_index('INDFISCAL', drop=False),
            gdf_copy[['area_construida_existente', gdf_copy.geometry.name, 'INDFISCAL']],
            how="left",
            predicate="intersects"
        )

        sjoin_result = sjoin_result[sjoin_result['INDFISCAL'] != sjoin_result['INDFISCAL_right']]

        medias_area = sjoin_result.groupby('INDFISCAL')['area_construida_existente_right'].mean().reset_index()
        medias_area.rename(columns={'area_construida_existente_right': 'MEDIA_AREA_VIZINHOS'}, inplace=True)

        gdf_copy = gdf_copy.merge(medias_area, on="INDFISCAL", how="left")
        gdf_copy['MEDIA_AREA_VIZINHOS'] = gdf_copy['MEDIA_AREA_VIZINHOS'].fillna(0)

        if 'buffer_geometry' in gdf_copy.columns:
            gdf_copy.drop(columns=['buffer_geometry'], inplace=True)
        if 'index_right' in gdf_copy.columns:
            gdf_copy.drop(columns=['index_right'], inplace=True)
        if 'INDFISCAL_right' in gdf_copy.columns:
            gdf_copy.drop(columns=['INDFISCAL_right'], inplace=True)
        
        return gdf_copy

    gdf_lotes = calcular_vizinhos_info_otimizado_internal(gdf_lotes)
    
    st.success("Dados carregados e pré-processados com sucesso!")
    return gdf_lotes

# --- Fim da função load_and_preprocess_data ---


# --- SEÇÃO 5: Definição de Regras para Sugestão de Potencial Construtivo (Sistema Especialista Puro) ---

def calcular_andares_sugeridos_regra(lote_data):
    ca_max = lote_data["CA_MAX"]
    area_total = lote_data["AREA_TOTAL"]
    zona = lote_data.get("ZONA", "DESCONHECIDA")
    taxa_ocupacao_max = lote_data.get("TAXA_OCUPACAO_MAX", 0.0)

    andares_base = 1

    if ca_max >= 4.0 and area_total >= 1000:
        andares_base = 8
    elif ca_max >= 2.0 and area_total >= 500:
        andares_base = 4
    elif ca_max >= 1.0 and area_total >= 200:
        andares_base = 2
    else:
        andares_base = 1

    if "EIXO ESTRUTURAL" in zona.upper() or \
       "EIXO NOVA CURITIBA" in zona.upper() or \
       "EIXO MARECHAL FLORIANO" in zona.upper() or \
       "EIXO PRES. AFFONSO CAMARGO" in zona.upper() or \
       "LINHA VERDE" in zona.upper() or \
       "EIXO DE ADENSAMENTO" in zona.upper() or \
       "EIXO CONECTOR" in zona.upper():
        andares_base += 2

    if "ZONA HISTORICA" in zona.upper():
        andares_base = min(andares_base, 5)
    
    # Nova regra: Limitar andares se a taxa de ocupação máxima for muito baixa
    if taxa_ocupacao_max > 0 and taxa_ocupacao_max < 30.0: # Ex: Zonas de preservação ou muito baixas
        andares_base = min(andares_base, 2) # Limita a 2 andares se a ocupação é restrita

    return max(0, andares_base) # Garante mínimo de 0 andares para casos de não construção (preservação)

def calcular_area_sugerida_regra(lote_data):
    ca_max = lote_data["CA_MAX"]
    area_total = lote_data["AREA_TOTAL"]
    area_construida_existente = lote_data["area_construida_existente"]
    zona = lote_data.get("ZONA", "DESCONHECIDA")
    taxa_ocupacao_max = lote_data.get("TAXA_OCUPACAO_MAX", 0.0)

    FATOR_APROVEITAMENTO_POTENCIAL = 0.8
    sugestao_bruta_ca = area_total * ca_max * FATOR_APROVEITAMENTO_POTENCIAL

    if "EIXO" in zona.upper() or "LINHA VERDE" in zona.upper() or "POLO" in zona.upper():
        sugestao_bruta_ca *= 1.1

    if "PRESERVAÇÃO AMBIENTAL" in lote_data.get("USOS_PERMITIDOS_ZONA_STRING", "").upper() or \
       "RECREAÇÃO PASSIVA" in lote_data.get("USOS_PERMITIDOS_ZONA_STRING", "").upper():
        return 0 # Zonas de preservação, sem área construída sugerida

    if area_construida_existente > 0:
        sugestao_ampliacao = area_construida_existente + (area_total * ca_max - area_construida_existente) * FATOR_APROVEITAMENTO_POTENCIAL
        if "EIXO" in zona.upper() or "LINHA VERDE" in zona.upper():
             sugestao_ampliacao *= 1.1
        sugestao_final_area = int(max(sugestao_ampliacao, sugestao_bruta_ca))
    else:
        sugestao_final_area = int(sugestao_bruta_ca)

    # Nova regra: A área sugerida não pode exceder a área total * taxa de ocupação máxima
    if taxa_ocupacao_max > 0:
        area_max_pela_ocupacao = area_total * (taxa_ocupacao_max / 100.0)
        sugestao_final_area = int(min(sugestao_final_area, area_max_pela_ocupacao))
    
    return max(0, sugestao_final_area) # Garante área não negativa

# --- SEÇÃO 6: Funções de Sugestão e Recomendações (Sistema Especialista Puro) ---

def sugerir_tipo_intervencao(lote_data, sugestao_area, sugestao_pavimentos):
    area_total = lote_data["AREA_TOTAL"]
    area_construida_existente = lote_data["area_construida_existente"]
    area_disponivel = lote_data["AREA_DISPONIVEL"]
    ca_real = lote_data["CA_REAL"]
    ca_max = lote_data["CA_MAX"]
    media_area_vizinhos = lote_data["MEDIA_AREA_VIZINHOS"]
    zona = lote_data.get("ZONA", "Desconhecida") 

    FATOR_GRANDE_AMPLIACAO = 1.5
    FATOR_NOVA_CONSTRUCAO = 2.0
    LIMIAR_CA_SUBUTILIZADO = 0.5
    LIMIAR_VIZINHOS_VAZIOS_PERCENTUAL = 0.02 # Influência dos vizinhos diminuída
    LIMIAR_AREA_MIN_EMPREENDIMENTO = 750

    if area_construida_existente > 0 and area_disponivel > 0 and ca_real < ca_max:
        if sugestao_area > area_construida_existente and \
           (sugestao_area / max(1, area_construida_existente)) < FATOR_NOVA_CONSTRUCAO:
            return "Ampliação da Construção Existente"

    if area_construida_existente > 0:
        if (ca_real < (LIMIAR_CA_SUBUTILIZADO * ca_max)) or \
           (sugestao_area > area_construida_existente and \
            (sugestao_area / max(1, area_construida_existente)) >= FATOR_NOVA_CONSTRUCAO):
            return "Nova Construção (Demolição e Reconstrução)"

    if ca_real < ca_max:
        vizinhos_muito_vazios = (media_area_vizinhos / max(1, area_total)) < LIMIAR_VIZINHOS_VAZIOS_PERCENTUAL
        sugestao_excede_lote_atual = (sugestao_area > (area_total * ca_max * 1.2)) and (sugestao_area > LIMIAR_AREA_MIN_EMPREENDIMENTO)
        zona_de_alto_adensamento = ("ADENSAMENTO" in zona.upper() or "GRANDES_USOS" in zona.upper() or "POLO" in zona.upper())

        if (vizinhos_muito_vazios and (zona_de_alto_adensamento or sugestao_excede_lote_atual)) or \
           sugestao_excede_lote_atual:
             return "Aquisição de Lotes do Entorno para Novo Empreendimento"

    if area_construida_existente == 0 or (area_construida_existente > 0 and ca_real >= ca_max and area_disponivel == 0 and sugestao_area > area_construida_existente):
        return "Nova Construção em Lote Vazio/Pouco Ocupado"

    return "Não Classificado / Análise Detalhada Necessária"

def fazer_sugestao_para_lote(lote_data_series):
    usos_permitidos_string = lote_data_series.get('USOS_PERMITIDOS_ZONA_STRING', '')
    
    if not isinstance(usos_permitidos_string, str) or not usos_permitidos_string.strip():
        sugestao_tipologia_display = 'Não Definido no Zoneamento'
    else:
        list_of_uses = [u.strip() for u in usos_permitidos_string.split(';') if u.strip()]
        
        sugestao_tipologia_display = 'Não Definido no Zoneamento'
        
        if list_of_uses:
            prioridade_usos = [
                "HABITAÇÃO UNIFAMILIAR", "HABITAÇÃO COLETIVA", "HABITAÇÃO INSTITUCIONAL", "HABITAÇÃO TRANSITÓRIA 1",
                "COMÉRCIO E SERVIÇO GERAL", "COMÉRCIO E SERVIÇO SETORIAL", "COMÉRCIO E SERVIÇO DE BAIRRO", "COMÉRCIO E SERVIÇO VICINAL",
                "INDÚSTRIA TIPO 1", "INDÚSTRIA TIPO 2", "INDÚSTRIA TIPO 3",
                "COMUNITÁRIO 1", "COMUNITÁRIO 2", "COMUNITÁRIO 3"
            ]
            
            for prior_use in prioridade_usos:
                if prior_use in list_of_uses:
                    sugestao_tipologia_display = prior_use
                    break
            
            if sugestao_tipologia_display == 'Não Definido no Zoneamento' and list_of_uses:
                sugestao_tipologia_display = list_of_uses[0]

    sugestao_pavimentos = calcular_andares_sugeridos_regra(lote_data_series)
    sugestao_area = calcular_area_sugerida_regra(lote_data_series)

    tipo_intervencao = sugerir_tipo_intervencao(lote_data_series, sugestao_area, sugestao_pavimentos)

    return {
        "tipologia_sugerida": sugestao_tipologia_display,
        "andares_sugeridos": sugestao_pavimentos,
        "area_sugerida": sugestao_area,
        "tipo_intervencao_sugerida": tipo_intervencao
    }


# --- Streamlit App ---

# O código do app Streamlit começa aqui, dentro da condição `elif pagina == "Estudo de Viabilidade":`
# Assumimos que 'pagina' é uma variável definida em um menu de navegação Streamlit.

# if 'pagina' not in st.session_state:
#     st.session_state.pagina = "Estudo de Viabilidade" # Define uma página padrão para teste

# if st.session_state.pagina == "Estudo de Viabilidade":
elif pagina == "Estudo de Viabilidade": # Conforme solicitado pelo usuário
    st.title("Estudo de Viabilidade")
    st.markdown("Faça uma simulação do melhor uso e ocupação para este lote.")

    # Carrega os dados uma vez e os armazena em cache
    with st.spinner("Carregando dados..."):
        gdf_lotes_app = load_and_preprocess_data()

    st.markdown("---")
    st.subheader("Análise de Lote por Indicação Fiscal")

    indfiscal_input = st.text_input("Digite a Indicação Fiscal (INDFISCAL) do lote para análise:", key="indfiscal_input").strip().upper()

    if st.button("Gerar Sugestão", key="generate_suggestion_button"):
        if indfiscal_input:
            lote_encontrado = gdf_lotes_app[gdf_lotes_app['INDFISCAL'] == indfiscal_input]

            if not lote_encontrado.empty:
                lote_para_sugestao_original_series = lote_encontrado.iloc[0]

                try:
                    sugestao_final = fazer_sugestao_para_lote(lote_para_sugestao_original_series)
                    
                    st.success(f"Sugestão Detalhada para o Lote INDFISCAL: {lote_para_sugestao_original_series['INDFISCAL']}")
                    st.write(f"**Tipologia Sugerida:** {sugestao_final['tipologia_sugerida']}")
                    st.write(f"**Andares Sugeridos:** {sugestao_final['andares_sugeridos']}")
                    st.write(f"**Área Sugerida:** {sugestao_final['area_sugerida']} m²")
                    st.write(f"**Tipo de Intervenção Sugerida:** {sugestao_final['tipo_intervencao_sugerida']}")
                    
                    st.markdown("---")
                    st.subheader("Dados do Lote (Para Comparação)")
                    st.write(f"- **Área Total do Lote:** {lote_para_sugestao_original_series['AREA_TOTAL']:.2f} m²")
                    st.write(f"- **Área Construída Existente:** {lote_para_sugestao_original_series['area_construida_existente']:.2f} m²")
                    st.write(f"- **CA Real:** {lote_para_sugestao_original_series['CA_REAL']:.2f}")
                    st.write(f"- **CA Máximo (Zoneamento):** {lote_para_sugestao_original_series['CA_MAX']:.2f}")
                    st.write(f"- **Taxa Ocupação Máx (Zoneamento):** {lote_para_sugestao_original_series.get('TAXA_OCUPACAO_MAX', 'N/A')}%")
                    st.write(f"- **Taxa Permeabilidade Mín (Zoneamento):** {lote_para_sugestao_original_series.get('TAXA_PERMEABILIDADE_MIN', 'N/A')}%")
                    st.write(f"- **Média Área Vizinhos:** {lote_para_sugestao_original_series['MEDIA_AREA_VIZINHOS']:.2f} m²")
                    st.write(f"- **Zona:** {lote_para_sugestao_original_series.get('ZONA', 'N/A')}")
                    st.write(f"- **Usos Permitidos na Zona (Completo):** {lote_para_sugestao_original_series.get('USOS_PERMITIDOS_ZONA_STRING', 'N/A')}")
                
                except Exception as e:
                    st.error(f"Erro ao gerar sugestão para a Indicação Fiscal {indfiscal_input}: {e}")
                    st.warning("Por favor, verifique se todos os dados necessários para o cálculo estão presentes para este lote.")
            else:
                st.warning(f"Indicação Fiscal '{indfiscal_input}' não encontrada no banco de dados de lotes.")
                st.info("Certifique-se de que a Indicação Fiscal está correta e existe no GeoJSON de Lotes.")
        else:
            st.info("Por favor, digite uma Indicação Fiscal para começar.")

# --- Fim do bloco elif pagina == "Estudo de Viabilidade": ---
