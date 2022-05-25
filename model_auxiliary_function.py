import pandas as pd
import streamlit as st

#######################
#Estadisticas Globales#
#######################
''' Funcion auxiliar que calcula las estadisticas globales (jugador/total_equipo) de las columnas (Player, Points, Rebounds, Assists, Turnovers, Steals) y lo guarda en un CSV. '''
def stats_global():
    days = ['2021-12-14', '2021-12-16', '2021-12-19', '2021-12-23', 
                          '2022-01-09', '2022-01-14',                             '2022-01-23', '2022-01-25', '2022-01-28',
            '2022-01-30', '2022-02-02', '2022-02-04', '2022-02-06', '2022-02-08', '2022-02-11', '2022-02-13', '2022-02-17',
            '2022-02-19', '2022-02-20', '2022-02-24', '2022-03-06', '2022-03-08', '2022-03-10', '2022-03-13', '2022-03-17',
            '2022-03-20', '2022-03-22', '2022-03-24', '2022-03-27', '2022-03-31', '2022-04-03', '2022-04-08', '2022-04-10',
            '2022-04-13', '2022-04-17', '2022-04-20', '2022-04-22', '2022-04-24', '2022-04-26']
    for day in days:
        #Leer CSV
        dataframe = pd.read_csv('data_' + str(day) + '/stats.csv')

        #Quitar columnas que no interesen
        dataframe = dataframe.iloc[: , 1:]     #Quitar primera columna
        dataframe = dataframe.drop(['Minutes', 'Field_percentage', 'Free_throw_percentage', 'Offensive_rebounds', 'Defensive_rebounds', 'Valoration'], axis=1)

        #Calcular el total de cada columna
        total_points = dataframe['Points'].sum()
        total_rebounds = dataframe['Rebounds'].sum()
        total_assists = dataframe['Assists'].sum()
        total_turnovers = dataframe['Turnovers'].sum()
        total_steals = dataframe['Steals'].sum()
        total_blocked_shots = dataframe['Blocked_shots'].sum()
        
        #Calcular las estadisticas globales (Estadistica jugador/Total equipo)
        dataframe['Puntos'] = round(dataframe['Points']/total_points, 5)
        dataframe['Rebotes'] = round(dataframe['Rebounds']/total_rebounds, 5)
        dataframe['Asistencias'] = round(dataframe['Assists']/total_assists, 5)
        dataframe['Perdidas'] = round(dataframe['Turnovers']/total_turnovers, 5)
        dataframe['Robos'] = round(dataframe['Steals']/total_steals, 5)
        dataframe['Tapones'] = round(dataframe['Blocked_shots']/total_blocked_shots, 5)
        
        #Quitar las columnas antiguas
        total_dataframe = dataframe.drop(['Points', 'Rebounds', 'Assists', 'Turnovers', 'Steals', 'Blocked_shots'], axis=1)
        #print(total_dataframe)
        #Guardar en CSV
        total_dataframe.to_csv('data_' + str(day) + '/stats_global.csv')
    print("Called stats_global()")

''' Funcion auxiliar que mete todas las estadisticas globales a un CSV. '''
def append_stats_global():
    days = ['2021-12-16', '2021-12-19', '2021-12-23', 
                          '2022-01-09', '2022-01-14',                             '2022-01-23', '2022-01-25', '2022-01-28',
            '2022-01-30', '2022-02-02', '2022-02-04', '2022-02-06', '2022-02-08', '2022-02-11', '2022-02-13', '2022-02-17',
            '2022-02-19', '2022-02-20', '2022-02-24', '2022-03-06', '2022-03-08', '2022-03-10', '2022-03-13', '2022-03-17',
            '2022-03-20', '2022-03-22', '2022-03-24', '2022-03-27', '2022-03-31', '2022-04-03', '2022-04-08', '2022-04-10',
            '2022-04-13', '2022-04-17', '2022-04-20', '2022-04-22', '2022-04-24', '2022-04-26']
    #Leer primer CSV para tener 1 cargado
    dataframe = pd.read_csv('data_2021-12-14/stats_global.csv')
    dataframe = dataframe.iloc[: , 1:]     #Quitar primera columna
    count = 0
    for i in days:
        #Se va leyendo CSV a CSV
        dataframe_auxiliar = pd.read_csv('data_' + str(i) + '/stats_global.csv')
        #Primera iteracion (Append a "dataframe")
        if count==0:
            resultado = dataframe.append(dataframe_auxiliar)
        #Las demás iteraciones (Append a "resultado")
        else:
            resultado = resultado.append(dataframe_auxiliar)
        count = count + 1
    resultado = resultado.iloc[:,:-1]       #Quitar ultima columna
    #Guardar CSV
    resultado.to_csv('Stats/StatsFull_global.csv')
    print(resultado)
    print("Called append_stats_global()")

''' Funcion que divide las estadisticas globales por posiciones. '''
def stats_by_position_global():
    #Dataframe estadisticas individuales/equipo
    dataframe = pd.read_csv('Stats/StatsFull_global.csv')
    dataframe = dataframe.iloc[: , 1:]     #Quitar primera columna

    #Pivots
    pivots = dataframe[dataframe['Player'].str.contains("Walter Tavares|Vincent Poirier")]
    pivots.to_csv('Stats/Stats_Pivots_global.csv')
    #Ala-Pivots
    ala_pivots = dataframe[dataframe['Player'].str.contains("Trey Thompkins|Guerschon Yabusele|Anthony Randolph")]
    ala_pivots.to_csv('Stats/Stats_AlaPivots_global.csv')
    #Aleros
    aleros = dataframe[dataframe['Player'].str.contains("Jeffery Taylor|Gabriel Deck|Adam Hanga|Alberto Abalde|Rudy Fernandez|Fabien Causeur")]
    aleros.to_csv('Stats/Stats_Aleros_global.csv')
    #Escoltas
    escoltas = dataframe[dataframe['Player'].str.contains("Jaycee Carroll")]
    escoltas.to_csv('Stats/Stats_Escoltas_global.csv')
    #Bases
    bases = dataframe[dataframe['Player'].str.contains("Sergio Llull|Carlos Alocen|Thomas Heurtel|Juan Nunez|Nigel Williams-Goss")]
    bases.to_csv('Stats/Stats_Bases_global.csv')
    print(len(pivots))
    print(len(ala_pivots))
    print(len(aleros))
    print(len(escoltas))
    print(len(bases))
    print("Called stats_by_position_global")

''' Funcion auxiliar que llama a todas las funciones principales para estadisticas globales. '''
def call_global():
    #1. Pasar las stats a stats globales de todos los jugadores (Necesita CSVs: stats.csv)
    stats_global()
    #2. Unir todas las stats globales a un CSV (Necesita CSVs: stats_global.csv)
    append_stats_global()
    #3. Dividir por posicion (Necesita CSV: StatsFull_global.csv) 
    stats_by_position_global()

#############
#Sentimiento#
#############
def sentiment_by_position():
    dataframe = pd.read_csv('Stats/SentimentFull.csv')
    #Pivots
    pivots = dataframe[dataframe['Player'].str.contains("Walter Tavares|Vincent Poirier")]
    pivots.to_csv('Stats/Sentiment_Pivots.csv')
    #Ala-Pivots
    ala_pivots = dataframe[dataframe['Player'].str.contains("Trey Thompkins|Guerschon Yabusele|Anthony Randolph")]
    ala_pivots.to_csv('Stats/Sentiment_AlaPivots.csv')
    #Aleros
    aleros = dataframe[dataframe['Player'].str.contains("Jeffery Taylor|Gabriel Deck|Adam Hanga|Alberto Abalde|Rudy Fernandez|Fabien Causeur")]
    aleros.to_csv('Stats/Sentiment_Aleros.csv')
    #Escoltas
    escoltas = dataframe[dataframe['Player'].str.contains("Jaycee Carroll")]
    escoltas.to_csv('Stats/Sentiment_Escoltas.csv')
    #Bases
    bases = dataframe[dataframe['Player'].str.contains("Sergio Llull|Carlos Alocen|Thomas Heurtel|Juan Nunez|Nigel Williams-Goss")]
    bases.to_csv('Stats/Sentiment_Bases.csv')

    print(len(pivots))
    print(len(ala_pivots))
    print(len(aleros))
    print(len(escoltas))
    print(len(bases))
    print("Called sentiment_by_position")

######
#MAIN#
######
if __name__ == "__main__":
    #Globales (individual/total)
    #call_global()
    print('')