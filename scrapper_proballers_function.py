import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
import os
import streamlit as st

''' Funcion para mandarselo a Beautifulsoup '''
def beauty_soup_fun(link):
    r = requests.get(link)
    soup = BeautifulSoup(r.text, 'lxml')
    return soup

''' Funcion para encontrar todos los links de los partidos '''
def calendar_function(search_day):
    proballers = 'https://www.proballers.com'
    link = 'https://www.proballers.com/es/baloncesto/equipo/160/real-madrid/calendario'
    soup = beauty_soup_fun(link)
    print("_Inicio calendar_function()")
    #count = 0
    games_url = []  #Array con el URL de todos los partidos
    games_day = []
    indice_buscado = 0

    table = soup.find_all('tr', itemtype="http://schema.org/SportsEvent")
    for game_day in table:
        url = game_day.find('a').attrs['href']
        full_url = proballers + url
        games_url.append(full_url)
        games_day.append(full_url[-10:])
        #print(str(count) + ": " + games_url[count])
        #print(str(count) + ": " + games_day[count])
        #count = count + 1

    #Si el dia que se quiere buscar esta dentro del array de dias
    if search_day in games_day:
        indice_buscado = games_day.index(search_day) + 1    #Se recoge el indice del partido para pasarselo al array "games_url" que contiene el url del partido en cuestion
        #print(indice_buscado)
    else:
        print("Game not found")
    return games_url[indice_buscado-1]      #Se devuelve el url del partido

''' Funcion para saber si el Real Madrid juega como visitante o local, y llama a "take_stats()" '''
def statistics(search_day):
    if os.path.exists('./data_'+ str(search_day) + '/stats.csv') == False:
        link = calendar_function(search_day)
        soup = beauty_soup_fun(link)
        print("_Inicio statistics()")
        
        #Llama a la funcion para escribir en la web
        scrapper_streamlit(search_day)

        #Primero hay que saber si el "Real Madrid" juega de visitante o de local (para saber si hay que buscar en la tabla de arriba o abajo)
        top_table = soup.find_all('h3', class_='team-title')[0]
        bottom_table = soup.find_all('h3', class_='team-title')[1]

        if(top_table.text == 'Real Madrid'):
            print('Real Madrid juega como local')
            top_team = soup.find_all('div', class_='home-game__content__entry home-game__content__team-stats__content-team-1')
            #print(top_team)
            statistics_data = take_stats(top_team, search_day)
        elif(bottom_table.text == 'Real Madrid'):
            print('Real Madrid juega como visitante')
            bottom_team = soup.find_all('div', class_='home-game__content__entry home-game__content__team-stats__content-team-2')
            #print(bottom_team)
            statistics_data = take_stats(bottom_team, search_day)
        else:
            print('Vacio')
            statistics_data = None
        print("Scrapeando")
    else:
        scrapper_streamlit(search_day)
        final_result = pd.read_csv('./data_'+ str(search_day) + '/stats.csv')
        pretty_final_resutl = final_result.iloc[: , 1:]     #Quitar primera columna
        st.dataframe(data=pretty_final_resutl, width=1200, height=600)
        print("Leido del CSV")
    #return statistics_data

''' Funcion que recoge todas las estadisticas del Real Madrid de la tabla '''
def take_stats(real_madrid_team, search_day):
    print("_Inicio take_stats()")
    array_stats = []
    for stats in real_madrid_team:
        players = stats.find_all('tr')
        #print(players)
        for stat_players in players:
            name = stat_players.find(class_='left first__left')                     #JUGADOR
            points = stat_players.find(class_='right highlight highlight--first')   #PTS
            rebounds = stat_players.find(class_='right highlight highlight')        #REB
            assists = stat_players.find(class_='right highlight highlight--last')   #AST
            minutes_played = stat_players.find_all(class_='right')[3]               #MIN
            field_percentage = stat_players.find_all(class_='right')[6]             #FG%
            free_trow_percentage = stat_players.find_all(class_='right')[8]         #1%
            offensive_rebounds = stat_players.find_all(class_='right')[9]           #RO
            defensive_rebounds = stat_players.find_all(class_='right')[10]          #RD
            turnovers = stat_players.find_all(class_='right')[13]                   #TE
            steals = stat_players.find_all(class_='right')[14]                      #BR
            blocket_shots = stat_players.find_all(class_='right')[15]               #TAP
            valoration = stat_players.find_all(class_='right')[-1]                  #VAL    -> siempre el ultimo elemento del array

            #Ifs necesarios para evitar el ultimo valor en el bucle
            if(name!=None): 
                clean_name = re.sub('\s\s', '', name.text)  #Se quitan los espacios
                clean_name = re.sub('^\s', '', clean_name) #Se quita el primer espacio
            else: clean_name = ""
            if(points!=None): text_points = points.text
            else: text_points = ""
            if(rebounds!=None): text_rebounds = rebounds.text
            else: text_rebounds = ""
            if(assists!=None): text_assists = assists.text
            else: text_assists = ""
            if(minutes_played!=None): text_minutes_played = minutes_played.text
            else: text_minutes_played = ""
            if(field_percentage!=None): text_field_percentage = field_percentage.text
            else: text_field_percentage = ""
            if(free_trow_percentage!=None): text_free_trow_percentage = free_trow_percentage.text
            else: text_free_trow_percentage = ""
            if(offensive_rebounds!=None): text_offensive_rebounds = offensive_rebounds.text
            else: text_offensive_rebounds = ""
            if(defensive_rebounds!=None): text_defensive_rebounds = defensive_rebounds.text
            else: text_defensive_rebounds = ""
            if(turnovers!=None): text_turnovers = turnovers.text
            else: text_turnovers = ""
            if(steals!=None): text_steals = steals.text
            else: text_steals = ""
            if(blocket_shots!=None): text_blocket_shots = blocket_shots.text
            else: text_blocket_shots = ""
            if(valoration!=None): text_valoration = valoration.text
            else: text_valoration = ""

            #print(str(clean_name), str(text_points), str(text_rebounds), str(text_assists), str(text_minutes_played), str(text_offensive_rebounds), str(text_defensive_rebounds), str(text_steals), str(text_blocket_shots), str(text_valoration))
            array_stats.append({
                'Player': clean_name,
                'Points': text_points,
                'Rebounds': text_rebounds,
                'Assists': text_assists,
                'Minutes': text_minutes_played,
                'Field_percentage': text_field_percentage,
                'Free_throw_percentage': text_free_trow_percentage,
                'Offensive_rebounds': text_offensive_rebounds,
                'Defensive_rebounds': text_defensive_rebounds,
                'Turnovers': text_turnovers,
                'Steals': text_steals,
                'Blocked_shots': text_blocket_shots,
                'Valoration': text_valoration
            })
        array_stats.pop()   #Quitar el ultimo elemento (pertenece al equipo en total y se recoge en otra funcion)
        array_stats.pop(0)  #Quitar el primer elemento (Leyenda)
    #final_result = json.dumps(array_stats, indent=3)
    final_result = pd.DataFrame(array_stats)
    st.dataframe(data=final_result, width=1200, height=600)
    #Guardar en csv
    if os.path.exists('./data_'+ str(search_day) + '/stats.csv') == False:
        final_result.to_csv('./data_'+ str(search_day) + '/stats.csv')
        print("Archivo creado")
    return final_result

''' Funcion que pinta los textos en streamlit para la pestaña de estadisticas'''
def scrapper_streamlit(search_day):
    st.write("""<h1 class="titulo-h1"> Estadisticas de los jugadores del Real Madrid para el partido del día """ + str(search_day), unsafe_allow_html=True)
    st.write("""<p class="contenido"> A continuación se muestra una tabla con las estadísticas de todos los <strong>jugadores</strong> que fueron convocados. 
    Si se hace scroll horizontal se pueden ver por completo las estadísticas, pudiendo ordenar cualquier campo tanto de manera ascendente como descendente. """, unsafe_allow_html=True)
    st.write("""<p class="contenido"> Estas estadísticas pertenecen al día """ + "<strong>" + str(search_day) + "</strong>:", unsafe_allow_html=True)
