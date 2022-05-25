from operator import index
import streamlit as st
import pandas as pd
from streamlit_folium import folium_static
import folium
from create_graph_function import sentiment_graph_streamlit
from scrapper_proballers_function import statistics
from ahp import model_function

from prediccion import prediction_model
from prediccion import prediction_stats_model

def settings_st():
    # Page settings
    st.set_page_config(
        page_title="TFG_Twitter_RM",
        page_icon="🏀",
        layout="wide",
        initial_sidebar_state="expanded",
        menu_items={'About':"""
            ## Author: 
            ## **Víctor Hernández Sanz**
            [Link to Github repository](https://github.com/victor00hs/TFG_Twitter)"""})
    # Style
    style = """ <style>
        /*Contenido de la pagina*/
            .appview-container{ background-color: #FFF6F0; }
            .block-container{ padding-top: 20px; }
        /*Sidebar*/
            .css-1adrfps{ background-color: #FFEBC3; }
        /*H1*/
            .h1-sidebar{ color: black; text-decoration: underline; padding: 0; font-variant: small-caps; font-weight: bold!important; }
            .titulo-h1{ text-align: center;  font-family: "Georgia"; color: black; }
            #inicio-h1{ text-align: justify;  font-family: "Georgia"; color: black; }
        /*st.write textos*/
            .contenido{ text-align: justify; }
        /*Tablas*/
            .col_heading{ background-color: #FFEBC3; text-color: black; }
            .row_heading { background-color: #FFEBC3; }
        /*Texto tablas*/
            .css-ps6290{ color: black; }
        /* Imagen */
            #img_logo{ display: block; margin-left: auto; margin-right: auto; width: 240px; }
        /*Footer*/
            footer{ visibility: hidden; }
        /* Mapa */
            iframe { position: relative; width: 100.0%; height: 500px; left: 0.0%; top: 0.0%; }
        /* imagen */
    </style> """
    st.markdown(style, unsafe_allow_html=True)

def main():
    #definir el array de los dias que se han recogido datos
    days = [                                                        '2021-12-14', '2021-12-16', '2021-12-19', '2021-12-23', 
                          '2022-01-09', '2022-01-14',                             '2022-01-23', '2022-01-25', '2022-01-28',
            '2022-01-30', '2022-02-02', '2022-02-04', '2022-02-06', '2022-02-08', '2022-02-11', '2022-02-13', '2022-02-17',
            '2022-02-19', '2022-02-20', '2022-02-24', '2022-03-06', '2022-03-08', '2022-03-10', '2022-03-13', '2022-03-17',
            '2022-03-20', '2022-03-22', '2022-03-24', '2022-03-27', '2022-03-31', '2022-04-03', '2022-04-08', '2022-04-10',
            '2022-04-13', '2022-04-17', '2022-04-20', '2022-04-22', '2022-04-24', '2022-04-26', '2022-05-01']
    #Selector de vista
    st.sidebar.write("""<h1 class="h1-sidebar">Seleccione una pestaña""", unsafe_allow_html=True)
    page = st.sidebar.selectbox(" ", ["Inicio", "Sentimiento", "Estadisticas Jugadores", "Modelo"])
    #Separador
    st.sidebar.write("___")
    #Selector de pestaña
    if page == "Inicio":
        inicio()
    elif page == "Sentimiento":
        st.sidebar.write("""<h1 class="h1-sidebar">Seleccione un día de partido""", unsafe_allow_html=True)
        day_selected = st.sidebar.selectbox(" ", days)
        #Cargar los dias
        data_sentiment = "data_" + str(day_selected) + "/total.json"
        print(day_selected)
        sentiment(data_sentiment)
    elif page == "Estadisticas Jugadores":
        st.sidebar.write("""<h1 class="h1-sidebar">Seleccione un día de partido""", unsafe_allow_html=True)
        day_selected = st.sidebar.selectbox(" ", days)
        #Cargar los dias
        data_sentiment = "data_" + str(day_selected) + "/total.json"
        print(day_selected)
        stats(day_selected)
    elif page == "Modelo":
        model()
    #Imagen escudo RM
    st.sidebar.write("""<img src='https://www.proballers.com/api/getTeamLogo?id=160' alt='Logo Real Madrid Baloncesto' 
                        id='img_logo'> """, unsafe_allow_html = True)

def inicio():
    st.write("""<h1 class="titulo-h1">EXTRACCIÓN DE INFORMACIÓN DE TWITTER PARA EL ANÁLISIS DE SENTIMIENTO Y POSICIONAMIENTO DE MARCA PERSONAL DE DEPORTISTAS PROFESIONALES""", unsafe_allow_html=True)
    st.write("""<div class="contenido">En esta web se pueden ver las estadisticas de los jugadores de baloncesto del Real Madrid, además de una valoración de sentimiento individual por jugador comprendida entre -1 y 1 de los tweets que los fans escriben en la red social de Twitter. Ambas caracteristicas están desglosadas por cada día de partido. 
                También se incluye un modelo de decisión multicriterio para conocer el jugador mejor valorado en la posición de juego y realizar una predicción del sentimiento para una valoración y un jugador seleccionado. """, unsafe_allow_html=True)
    st.write("""<div class="contenido">Para acceder a la información mencionada anteriormente, en la barra vertical de la izquierda se puede elegir la pestaña que se desee visualizar, además de poder seleccionar el día del cual se quiere ver la información.""", unsafe_allow_html=True)
    st.write("""<div class="contenido">Mapa de la localización del <strong>Wizink Center</strong>:""", unsafe_allow_html=True)
    #Mapa del Wizink Center
    lat, lon = 40.423889160, -3.671667099
    m = folium.Map(location=[lat, lon], zoom_start=17)
    folium.Marker([lat, lon], popup='Wizink Center', tooltip='Wizink Center', icon=folium.Icon(color="red", icon="glyphicon glyphicon-flag"),).add_to(m)
    folium.CircleMarker( location=[lat, lon], radius=100, popup="Wizink Center", color="blue", fill=True, tooltip='Wizink Center', fill_color="#14c4e3",).add_to(m)
    folium_static(m)

def sentiment(data_sentiment):
    sentiment_graph_streamlit(data_sentiment)

def stats(data_stats):
    statistics(data_stats)

def model():
    st.write("""<h1 class="titulo-h1">Modelos""", unsafe_allow_html=True)
    st.write("""<div class="contenido">Selecciona una posición la cual quieras obtener los datos calculados con el modelo de clasificación AHP. """, unsafe_allow_html=True)
    option = st.selectbox("", ['Bases', 'Pivots', 'Aleros', 'AlaPivots', 'Escoltas'])
    if option == 'Pivots':
        position = 'Model/AHP_Pivots.csv'
        model_function(position, basket_pos='Pivots')
    if option == 'Aleros':
        position = 'Model/AHP_Aleros.csv'
        model_function(position, basket_pos='Aleros')
    if option == 'AlaPivots':
        position = 'Model/AHP_AlaPivots.csv'
        model_function(position, basket_pos='Ala Pivots')
    if option == 'Bases':
        position = 'Model/AHP_Bases.csv'
        model_function(position, basket_pos='Bases')
    if option == 'Escoltas':
        position = 'Model/AHP_Escoltas.csv'
        model_function(position, basket_pos='Escoltas')
    #Modelo prediccion
    if option != 'Escoltas':
        st.header("Modelo Predictivo para los " + str(option))
        model_type = st.selectbox("Selecciona el criterio para realizar la predicción: ", ['Valoracion global', 'Estadisticas'], key='model_type')
        if model_type == "Valoracion global":
            prediction_model(option)
        elif model_type == "Estadisticas":
            prediction_stats_model(option)


if __name__ == "__main__":
    settings_st()
    main()
