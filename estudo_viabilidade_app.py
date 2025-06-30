import streamlit as st
import pandas as pd
import geopandas as gpd
import numpy as np

# --- Funções de cálculo do sistema especialista ---
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

    if any(eixo in zona.upper() for eixo in ["EIXO ESTRUTURAL", "EIXO NOVA CURITIBA", "EIXO MARECHAL FLORIANO", "EIXO PRES. AFFONSO CAMARGO", "LINHA VERDE", "EIXO DE ADENSAMENTO", "EIXO CONECTOR"]):
        andares_base += 2

    if "ZONA HISTORICA" in zona.upper():
        andares_base = min(andares_base, 5)

    if 0 < taxa_ocupacao_max < 30.0:
        andares_base = min(andares_base, 2)

    return max(0, andares_base)

def calcular_area_sugerida_regra(lote_data):
    ca_max = lote_data["CA_MAX"]
    area_total = lote_data["AREA_TOTAL"]
    area_construida_existente = lote_data["area_construida_existente"]
    zona = lote_data.get("ZONA", "DESCONHECIDA")
    taxa_ocupacao_max = lote_data.get("TAXA_OCUPACAO_MAX", 0.0)

    FATOR = 0.8
    sugestao_ca = area_total * ca_max * FATOR

    if any(eixo in zona.upper() for eixo in ["EIXO", "LINHA VERDE", "POLO"]):
        sugestao_ca *= 1.1

    usos = lote_data.get("USOS_PERMITIDOS_ZONA_STRING", "")
    if any(palavra in usos.upper() for palavra in ["PRESERVAÇÃO", "RECREAÇÃO"]):
        return 0

    if area_construida_existente > 0:
        ampliacao = area_construida_existente + (area_total * ca_max - area_construida_existente) * FATOR
        if any(eixo in zona.upper() for eixo in ["EIXO", "LINHA VERDE"]):
            ampliacao *= 1.1
        sugestao = int(max(ampliacao, sugestao_ca))
    else:
        sugestao = int(sugestao_ca)

    if taxa_ocupacao_max > 0:
        limite_ocupacao = area_total * (taxa_ocupacao_max / 100.0)
        sugestao = int(min(sugestao, limite_ocupacao))

    return max(0, sugestao)

def sugerir_tipo_intervencao(lote_data, sugestao_area, sugestao_pavimentos):
    area_total = lote_data["AREA_TOTAL"]
    area_construida = lote_data["area_construida_existente"]
    area_disponivel = lote_data["AREA_DISPONIVEL"]
    ca_real = lote_data["CA_REAL"]
    ca_max = lote_data["CA_MAX"]
    media_vizinhos = lote_data["MEDIA_AREA_VIZINHOS"]
    zona = lote_data.get("ZONA", "Desconhecida")

    FATOR_AMPLIACAO = 1.5
    FATOR_NOVA = 2.0
    CA_SUBUTILIZADO = 0.5
    PCT_VIZIOS = 0.02
    MIN_EMPREEND = 750

    if area_construida > 0 and area_disponivel > 0 and ca_real < ca_max:
        if sugestao_area > area_construida and (sugestao_area / max(1, area_construida)) < FATOR_NOVA:
            return "Ampliação da Construção Existente"

    if area_construida > 0:
        if (ca_real < CA_SUBUTILIZADO * ca_max) or (sugestao_area > area_construida and sugestao_area / max(1, area_construida) >= FATOR_NOVA):
            return "Nova Construção (Demolição e Reconstrução)"

    if ca_real < ca_max:
        vizinhos_vazios = (media_vizinhos / max(1, area_total)) < PCT_VIZIOS
        excede_ca = sugestao_area > area_total * ca_max * 1.2 and sugestao_area > MIN_EMPREEND
        adensamento = any(x in zona.upper() for x in ["ADENSAMENTO", "GRANDES_USOS", "POLO"])
        if (vizinhos_vazios and (adensamento or excede_ca)) or excede_ca:
            return "Aquisição de Lotes do Entorno para Novo Empreendimento"

    if area_construida == 0 or (area_construida > 0 and ca_real >= ca_max and area_disponivel == 0 and sugestao_area > area_construida):
        return "Nova Construção em Lote Vazio/Pouco Ocupado"

    return "Não Classificado / Análise Detalhada Necessária"

def fazer_sugestao_para_lote(lote_data):
    usos = lote_data.get('USOS_PERMITIDOS_ZONA_STRING', '')
    usos_list = [u.strip().upper() for u in usos.split(';') if u.strip()] if isinstance(usos, str) else []

    prioridades = [
        "HABITAÇÃO UNIFAMILIAR", "HABITAÇÃO COLETIVA", "HABITAÇÃO INSTITUCIONAL", "HABITAÇÃO TRANSITÓRIA 1",
        "COMÉRCIO E SERVIÇO GERAL", "COMÉRCIO E SERVIÇO SETORIAL", "COMÉRCIO E SERVIÇO DE BAIRRO", "COMÉRCIO E SERVIÇO VICINAL",
        "INDÚSTRIA TIPO 1", "INDÚSTRIA TIPO 2", "INDÚSTRIA TIPO 3",
        "COMUNITÁRIO 1", "COMUNITÁRIO 2", "COMUNITÁRIO 3"
    ]

    tipologia = next((uso for uso in prioridades if uso in usos_list), usos_list[0] if usos_list else "Não Definido no Zoneamento")

    andares = calcular_andares_sugeridos_regra(lote_data)
    area = calcular_area_sugerida_regra(lote_data)
    intervencao = sugerir_tipo_intervencao(lote_data, area, andares)

    return {
        "tipologia_sugerida": tipologia,
        "andares_sugeridos": andares,
        "area_sugerida": area,
        "tipo_intervencao_sugerida": intervencao
    }
