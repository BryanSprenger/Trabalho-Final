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
  def main():
	st.title("Como adicionar mapas no StreamLit")
	st.subheader("Baseado num caderno do Colab")
	menu = ["Home","Mapa"]
	choice = st.sidebar.selectbox('Menu',menu)
	if choice == 'Home':
		st.subheader("Página Inicial 1")
	elif choice == 'Mapa':
		st.subheader("Visualizar Mapa")
		with st.echo():
			m = folium.Map (location = [-25.5,-49.3], zoom_start =  9)
			folium_static(m)
	else: 
		st.subheader("")
if __name__ == '__main__':
	main()
