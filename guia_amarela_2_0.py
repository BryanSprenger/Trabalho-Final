import streamlit as st
from streamlit_folium import st_folium
import folium
import geopandas as gpd
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from folium.plugins import Fullscreen, MeasureControl, MiniMap
from estudo_viabilidade_app import fazer_sugestao_para_lote


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
# --- Campo de Indicação Fiscal Global ---
with st.sidebar:
    st.markdown("### 🔍 Consulta de Lote")
    st.text_input("Digite a Indicação Fiscal (INDFISCAL):", key="indfiscal_global")

# Menu lateral
st.sidebar.title("Navegação")
pagina = st.sidebar.radio(
    "Selecione uma seção:",
    (
        "🏠 Home",
        "🏗️ Potencial Construtivo",
        "📐 Área de Ocupação",
        "📊 Indicadores Urbanísticos",
        "🗺️ Mapa Interativo",
        "🏘️ Análise Estatística de Emissão de Alvarás",
        #"🧮 Estudo de Viabilidade" 
    )
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

    ind_fiscal = st.session_state.get("indfiscal_global", "").strip().upper()
   
    if ind_fiscal:
        gdf_lotes["INDFISCAL"] = gdf_lotes["INDFISCAL"].astype(str)
        lote_selecionado = gdf_lotes[gdf_lotes["INDFISCAL"] == ind_fiscal]

        if lote_selecionado.empty:
            st.warning("⚠️ Nenhum lote encontrado com essa Indicação Fiscal.")
        else:
            area_m2 = lote_selecionado.geometry.area.iloc[0]
            st.success(f"✅ Área do lote: **{area_m2:.2f} m²**")

            geom_lote = lote_selecionado.geometry.values[0]

            if geom_lote.is_empty:
                st.error("A geometria do lote está vazia.")
            elif geom_lote.geom_type == "MultiPolygon":
                geom_lote = max(geom_lote.geoms, key=lambda a: a.area)

            # Define origem no ponto mais ao sul
            coords = list(geom_lote.exterior.coords)
            ponto_base = min(coords, key=lambda pt: pt[1])  # menor latitude
            x_base, y_base = ponto_base

            # Translada coordenadas em relação ao ponto mais ao sul
            coords_transladadas = [(x - x_base, y - y_base) for x, y in coords]

            # Alinha a geometria para que a maior dimensão fique paralela ao eixo X
            coords_array = np.array(coords_transladadas)
            x_arr, y_arr = coords_array[:, 0], coords_array[:, 1]
            cov = np.cov(x_arr, y_arr)
            eig_vals, eig_vecs = np.linalg.eigh(cov)
            principal_axis = eig_vecs[:, np.argmax(eig_vals)]
            angulo = np.arctan2(principal_axis[1], principal_axis[0])
            cos_ang, sin_ang = np.cos(-angulo), np.sin(-angulo)

            coords_rotacionadas = [
                (x * cos_ang - y * sin_ang, x * sin_ang + y * cos_ang)
                for x, y in coords_transladadas
            ]

            # Obtém o CA da zona
            zona_intersectada = gdf_zonas[gdf_zonas.intersects(geom_lote)]
            if not zona_intersectada.empty:
                zona_nome = zona_intersectada.iloc[0]["NM_ZONA"]
                zona_match = df_zoneamento_indices[df_zoneamento_indices["ZONA"] == zona_nome]

                if not zona_match.empty:
                    ca_max = float(zona_match["CA_MAXIMO"].values[0])
                    st.info(f"🏙️ Zona: **{zona_nome}** — CA Máximo: **{ca_max}**")

                    ca = st.slider("Coeficiente de Aproveitamento (CA)", 0.1, ca_max, min(1.0, ca_max), 0.1)
                    altura = (ca * area_m2) / (area_m2 ** 0.5)

                    x, y = zip(*coords_rotacionadas)
                    z_base = [0] * len(x)
                    z_top = [altura] * len(x)

                    fig = go.Figure()

                    fig.add_trace(go.Scatter3d(x=x, y=y, z=z_base, mode='lines',
                                               line=dict(color='blue', width=4), name='Base'))
                    fig.add_trace(go.Scatter3d(x=x, y=y, z=z_top, mode='lines',
                                               line=dict(color='lightblue', width=4), name='Topo'))

                    for i in range(len(x)):
                        fig.add_trace(go.Scatter3d(
                            x=[x[i], x[i]], y=[y[i], y[i]], z=[0, altura],
                            mode='lines', line=dict(color='lightblue', width=2), showlegend=False
                        ))

                    fig.update_layout(
                        scene=dict(
                            xaxis_title='Distância X (m)',
                            yaxis_title='Distância Y (m)',
                            zaxis_title='Altura (m)',
                            aspectmode='data'
                        ),
                        margin=dict(l=0, r=0, b=0, t=30)
                    )

                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.warning("⚠️ Zona identificada no mapa, mas não localizada na tabela de índices.")
            else:
                st.warning("⚠️ A zona correspondente ao lote não foi identificada no mapa.")
    else:
        st.info("Digite uma Indicação Fiscal para iniciar.")

# --------------------------------------------------------------------------------------- ÁREA DE OCUPAÇÃO -------------------------------------------------------------------

elif pagina == "📐 Área de Ocupação":
    st.title("📐 Área de Ocupação do Lote")
    st.markdown("Visualize o quanto do lote pode ser ocupado com base na taxa de ocupação da zona urbanística correspondente.")

    ind_fiscal_2 = st.session_state.get("indfiscal_global", "").strip().upper()

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
                    area_total = geom.area
                    st.markdown(f"**📏 Área total do lote:** {area_total:.2f} m²")

                    coords = np.array(geom.exterior.coords)
                    # Referência sul: menor Y
                    ref_point = coords[np.argmin(coords[:, 1])]
                    coords_transladadas = coords - ref_point

                    # Rotação para alinhar o lado mais comprido com X
                    delta = coords_transladadas[-1] - coords_transladadas[0]
                    angle = np.arctan2(delta[1], delta[0])
                    rot_matrix = np.array([
                        [np.cos(-angle), -np.sin(-angle)],
                        [np.sin(-angle), np.cos(-angle)]
                    ])
                    coords_rotacionadas = coords_transladadas @ rot_matrix.T

                    x = coords_rotacionadas[:, 0].tolist()
                    y = coords_rotacionadas[:, 1].tolist()

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
                            altura = 3  # simbólica

                            # Escala para a projeção ocupada
                            escala = (area_ocupada / area_total) ** 0.5
                            x_centro = sum(x) / len(x)
                            y_centro = sum(y) / len(y)
                            x_scaled = [(xi - x_centro) * escala + x_centro for xi in x]
                            y_scaled = [(yi - y_centro) * escala + y_centro for yi in y]
                            z_base = [0] * len(x)
                            z_top = [altura] * len(x)

                            fig2 = go.Figure()

                            # Lote original
                            fig2.add_trace(go.Scatter3d(
                                x=x, y=y, z=z_base, mode='lines',
                                line=dict(color='lightgray', width=3),
                                name='Área Total'
                            ))

                            # Ocupação simulada
                            fig2.add_trace(go.Scatter3d(
                                x=x_scaled, y=y_scaled, z=z_top, mode='lines',
                                line=dict(color='green', width=4),
                                name=f'Ocupação ({ocupacao_pct}%)'
                            ))

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
                                    xaxis_title="Distância (m)",
                                    yaxis_title="Distância (m)",
                                    zaxis_title="Altura (m)"
                                ),
                                margin=dict(l=0, r=0, t=30, b=0)
                            )

                            st.plotly_chart(fig2, use_container_width=True)

                            # Pizza
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
        indfiscal_zona = st.session_state.get("indfiscal_global", "").strip().upper()

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
    ind_fiscal_map = st.session_state.get("indfiscal_global", "").strip().upper()

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

    anos_disponiveis = sorted(list(urls_alvaras.keys()), key=lambda x: int(x))

    # Timeline com slider
    ano_selecionado = st.slider(
        "Selecione o ano do relatório de alvarás:",
        min_value=int(anos_disponiveis[0]),
        max_value=int(anos_disponiveis[-1]),
        step=1,
        value=int(anos_disponiveis[-1]),
        format="%d"
    )
    ano_selecionado = str(ano_selecionado)
    url_csv = urls_alvaras[ano_selecionado]

    # Carregamento dos dados de alvarás
    try:
        df_alvaras = pd.read_csv(url_csv, sep=';', encoding='utf-8')
        st.success(f"Relatório de alvarás de {ano_selecionado} carregado com sucesso.")
    except Exception as e:
        st.error(f"Erro ao carregar os dados do relatório: {e}")
        st.stop()

    # Padronização dos dados
    if 'INDFISCAL' not in df_alvaras.columns:
        st.error("❌ A coluna 'INDFISCAL' não foi encontrada no CSV dos alvarás.")
        st.stop()

    df_alvaras['INDFISCAL'] = df_alvaras['INDFISCAL'].astype(str).str.replace('.', '', regex=False)

    if 'INDFISCAL' not in gdf_lotes.columns:
        st.error("❌ A coluna 'INDFISCAL' não foi encontrada nos dados dos lotes.")
        st.stop()
    else:
        gdf_lotes['INDFISCAL'] = gdf_lotes['INDFISCAL'].astype(str)

    # Cruzamento entre alvarás e lotes
    gdf_alvaras_lotes = gdf_lotes.merge(df_alvaras, on='INDFISCAL', how='inner')

    # Verificação da INDFISCAL digitada
    indfiscal_lote = st.session_state.get("indfiscal_global", "").strip().upper()
    indfiscal_conjunto_alvaras = set(df_alvaras['INDFISCAL'].unique())

    if indfiscal_lote:
        if indfiscal_lote in indfiscal_conjunto_alvaras:
            st.info(f"🔍 A indicação fiscal **{indfiscal_lote}** está presente no conjunto de alvarás de {ano_selecionado}.")
        else:
            st.warning(f"⚠️ A indicação fiscal **{indfiscal_lote}** **não** foi encontrada nos alvarás deste ano.")

    num_cruzamentos = len(gdf_alvaras_lotes)
    if num_cruzamentos > 0:
        st.success(f"✅ Foram encontrados {num_cruzamentos} cruzamentos entre lotes e alvarás.")
    else:
        st.warning("⚠️ Nenhum cruzamento entre lotes e alvarás foi encontrado.")

    # Mapa interativo
    if num_cruzamentos > 0 and 'Uso(s) Alvará' in gdf_alvaras_lotes.columns:
        st.markdown("### 🗺️ Visualização dos Lotes com Alvarás Emitidos por Uso")

        m_alvaras = folium.Map(location=[-25.42, -49.25], zoom_start=13, tiles='CartoDB positron')

        usos = gdf_alvaras_lotes['Uso(s) Alvará'].unique()
        cores = px.colors.qualitative.Safe
        cores_dict = {uso: cores[i % len(cores)] for i, uso in enumerate(usos)}

        folium.GeoJson(
            gdf_alvaras_lotes,
            name="Lotes com Alvará",
            tooltip=folium.GeoJsonTooltip(
                fields=["INDFISCAL", "Uso(s) Alvará"],
                aliases=["Indicação Fiscal", "Uso"],
                sticky=True
            ),
            style_function=lambda feature: {
                "fillColor": cores_dict.get(feature["properties"].get("Uso(s) Alvará", ""), "gray"),
                "color": "black",
                "weight": 1,
                "fillOpacity": 0.5
            }
        ).add_to(m_alvaras)

        folium.LayerControl().add_to(m_alvaras)
        st_folium(m_alvaras, width="100%", height=700)

    elif num_cruzamentos > 0:
        st.warning("⚠️ A coluna 'Uso(s) Alvará' não foi encontrada nos dados cruzados.")

    # Gráfico de barras com distribuição por uso
    if 'Uso(s) Alvará' in df_alvaras.columns:
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



#---------------------------------------------------------- ESTUDO DE VIABILIDADE --------------------------------------------------------------
# O código do estudo de viabilidade será inserido futuramente.
