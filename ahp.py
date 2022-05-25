import pandas as pd
import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt

def model_ahp(stats_file, sentiment_file, result_file):
    #Declaracion de los valores de los criterios 
    puntos_rebotes = round(9, 3)
    puntos_asist = round(1, 3)
    puntos_tapon = round(9, 3)
    puntos_robos = round(7, 3)

    rebotes_asist = round(1/3, 3)
    rebotes_tapon = round(3, 3)
    rebotes_robos = round(3, 3)

    asist_tapones = round(9, 3)
    asist_robos = round(9, 3)

    tapon_robos = round(1/3, 3)
    #Numero de criterios
    num_criterios = 5

    #Matriz comparando criterios
    df = pd.DataFrame([
            [round(1, 3),                puntos_rebotes,            puntos_asist,               puntos_tapon,            puntos_robos],
            [round(1/puntos_rebotes, 3), round(1, 3),               rebotes_asist,              rebotes_tapon,           rebotes_robos],
            [round(1/puntos_asist, 3),   round(1/rebotes_asist, 3), round(1, 3),                asist_tapones,           asist_robos],
            [round(1/puntos_tapon, 3),   round(1/rebotes_tapon, 3), round(1/asist_tapones, 3),  round(1, 3),             tapon_robos],
            [round(1/puntos_robos, 3),   round(1/rebotes_robos, 3), round(1/asist_robos, 3),    round(1/tapon_robos, 3), round(1, 3)]], 
            columns=['Puntos', 'Rebotes', 'Asistencias', 'Tapones', 'Robos'])
    #print('Matriz: \n', df )

    #Sumatorio columnas
    suma_puntos = df['Puntos'].sum()
    suma_rebotes = df['Rebotes'].sum()
    suma_Asistencias = df['Asistencias'].sum()
    suma_Tapones = df['Tapones'].sum()
    suma_Robos = df['Robos'].sum()

    #Matriz normalizada
    matriz_normalizada = pd.DataFrame([
            [(df['Puntos'].loc[0]/suma_puntos), (df['Rebotes'].loc[0]/suma_rebotes), (df['Asistencias'].loc[0]/suma_Asistencias), (df['Tapones'].loc[0]/suma_Tapones), (df['Robos'].loc[0]/suma_Robos)],
            [(df['Puntos'].loc[1]/suma_puntos), (df['Rebotes'].loc[1]/suma_rebotes), (df['Asistencias'].loc[1]/suma_Asistencias), (df['Tapones'].loc[1]/suma_Tapones), (df['Robos'].loc[1]/suma_Robos)],
            [(df['Puntos'].loc[2]/suma_puntos), (df['Rebotes'].loc[2]/suma_rebotes), (df['Asistencias'].loc[2]/suma_Asistencias), (df['Tapones'].loc[2]/suma_Tapones), (df['Robos'].loc[2]/suma_Robos)],
            [(df['Puntos'].loc[3]/suma_puntos), (df['Rebotes'].loc[3]/suma_rebotes), (df['Asistencias'].loc[3]/suma_Asistencias), (df['Tapones'].loc[3]/suma_Tapones), (df['Robos'].loc[3]/suma_Robos)],
            [(df['Puntos'].loc[4]/suma_puntos), (df['Rebotes'].loc[4]/suma_rebotes), (df['Asistencias'].loc[4]/suma_Asistencias), (df['Tapones'].loc[4]/suma_Tapones), (df['Robos'].loc[4]/suma_Robos)]])
    #print('Matriz normalizada: \n', matriz_normalizada)

    #Promedio de la matriz normalizada
    promedio_puntos = (matriz_normalizada[0].loc[0] + matriz_normalizada[1].loc[0] + matriz_normalizada[2].loc[0] + matriz_normalizada[3].loc[0] +matriz_normalizada[4].loc[0])/num_criterios
    promedio_rebotes = (matriz_normalizada[0].loc[1] + matriz_normalizada[1].loc[1] + matriz_normalizada[2].loc[1] + matriz_normalizada[3].loc[1] +matriz_normalizada[4].loc[1])/num_criterios
    promedio_asistencias = (matriz_normalizada[0].loc[2] + matriz_normalizada[1].loc[2] + matriz_normalizada[2].loc[2] + matriz_normalizada[3].loc[2] +matriz_normalizada[4].loc[2])/num_criterios
    promedio_tapones = (matriz_normalizada[0].loc[3] + matriz_normalizada[1].loc[3] + matriz_normalizada[2].loc[3] + matriz_normalizada[3].loc[3] +matriz_normalizada[4].loc[3])/num_criterios
    promedio_robos = (matriz_normalizada[0].loc[4] + matriz_normalizada[1].loc[4] + matriz_normalizada[2].loc[4] + matriz_normalizada[3].loc[4] +matriz_normalizada[4].loc[4])/num_criterios

    #Vector ponderacion
    matriz_ponderacion = pd.DataFrame([
        [promedio_puntos],
        [promedio_rebotes],
        [promedio_asistencias],
        [promedio_tapones],
        [promedio_robos]])
    print('Matriz ponderación: \n', matriz_ponderacion)

    #Relacion de consistencia
    matriz_relacion_consistencia = pd.DataFrame([
        [ (df['Puntos'].loc[0] * matriz_ponderacion[0].loc[0]) + (df['Rebotes'].loc[0] * matriz_ponderacion[0].loc[1]) + (df['Asistencias'].loc[0] * matriz_ponderacion[0].loc[2]) + (df['Tapones'].loc[0] * matriz_ponderacion[0].loc[3] + df['Robos'].loc[0] * matriz_ponderacion[0].loc[4])],
        [ (df['Puntos'].loc[1] * matriz_ponderacion[0].loc[0]) + (df['Rebotes'].loc[1] * matriz_ponderacion[0].loc[1]) + (df['Asistencias'].loc[1] * matriz_ponderacion[0].loc[2]) + (df['Tapones'].loc[1] * matriz_ponderacion[0].loc[3] + df['Robos'].loc[1] * matriz_ponderacion[0].loc[4])],
        [ (df['Puntos'].loc[2] * matriz_ponderacion[0].loc[0]) + (df['Rebotes'].loc[2] * matriz_ponderacion[0].loc[1]) + (df['Asistencias'].loc[2] * matriz_ponderacion[0].loc[2]) + (df['Tapones'].loc[2] * matriz_ponderacion[0].loc[3] + df['Robos'].loc[2] * matriz_ponderacion[0].loc[4])],
        [ (df['Puntos'].loc[3] * matriz_ponderacion[0].loc[0]) + (df['Rebotes'].loc[3] * matriz_ponderacion[0].loc[1]) + (df['Asistencias'].loc[3] * matriz_ponderacion[0].loc[2]) + (df['Tapones'].loc[3] * matriz_ponderacion[0].loc[3] + df['Robos'].loc[3] * matriz_ponderacion[0].loc[4])],
        [ (df['Puntos'].loc[4] * matriz_ponderacion[0].loc[0]) + (df['Rebotes'].loc[4] * matriz_ponderacion[0].loc[1]) + (df['Asistencias'].loc[4] * matriz_ponderacion[0].loc[2]) + (df['Tapones'].loc[4] * matriz_ponderacion[0].loc[3] + df['Robos'].loc[4] * matriz_ponderacion[0].loc[4])]
    ])
    #print('Vector relación consistencia (Matriz*Ponderacion):\n', matriz_relacion_consistencia)
    total_relacion_consistencia = matriz_relacion_consistencia[0].sum()
    #print('Total relación consistencia: ', total_relacion_consistencia, '\n')

    #Indice de consistencia
    ci = (total_relacion_consistencia-num_criterios)/(num_criterios-1)

    #Consistencia aleatoria
    ri = (1.98*(num_criterios-2)/num_criterios)

    #Relacion de consistencia
    cr = ci/ri
    print('Relación de consistencia: ', cr)

    #Leer estadisticas
    stats_df = pd.read_csv(stats_file)
    stats_df = stats_df.iloc[: , 1:]     #Quitar primera columna
    stats_df = stats_df.drop(['Perdidas'], axis=1)

    lista = []
    #Calcular la valoracion aplicando el modelo
    for i in stats_df.index:
        fila_operacion = matriz_ponderacion[0][0] * stats_df['Puntos'][i] + matriz_ponderacion[0][1] * stats_df['Rebotes'][i] + matriz_ponderacion[0][2] * stats_df['Asistencias'][i] + matriz_ponderacion[0][3] * stats_df['Tapones'][i] +matriz_ponderacion[0][4] * stats_df['Robos'][i]
        #print(fila_operacion)
        lista.append(fila_operacion)
    valoracion_ahp_df = pd.DataFrame(lista, columns = ['Stats_Valoration'])
    print(valoracion_ahp_df)

    #Añadir el sentimiento al mismo dataframe
    sentiment_df = pd.read_csv(sentiment_file)
    sentiment_df = sentiment_df.iloc[: , 1:]     #Quitar primera columna
    sentiment_df['Stats_Valoration'] = round(valoracion_ahp_df['Stats_Valoration'], 3)
    print(sentiment_df)
    sentiment_df.to_csv(result_file, index=False)

''' Funcion del modelo que pinta en la pagina web con streamlit. '''
def model_function(position, basket_pos):
    #Guardar el sentimiento y valoración AHP individual
    rank = pd.read_csv(position)
    rank = rank.sort_values(["Stats_Valoration", "Valoration"], ascending = (False, False))
    rank.rename(columns={'Player':'Jugador', 'Valoration': 'Sentimiento', 'Game_Day': 'Dia', 'Stats_Valoration': 'Valoración'}, inplace=True)   #Renombrar columnas
    rank = rank.assign(no_index='').set_index('no_index')       #Quitar el indice que sale por defecto en streamlit

    #Guardar el sentimiento y valoración AHP agrupado por jugador
    df_group = pd.read_csv(position)
    df_group = df_group.groupby(['Player']).mean()
    df_group.rename(columns={'Valoration': 'Sentimiento', 'Stats_Valoration': 'Valoración'}, inplace=True)

    col1, col2 = st.columns(2)
    #Columna izquierda
    with col1:
        st.header("Modelo AHP individual por partido ")
        if len(rank) != 0:
            st.dataframe(data=rank, width=600, height=505)
        else:
            st.write("""<div class="contenido">No hay datos para la posición seleccionada. """, unsafe_allow_html=True)
    #Columna derecha
    with col2:
        st.header("Ranking de los " + str(basket_pos))
        if len(df_group) != 0:
            st.dataframe(data=df_group, width=600, height=480)
            fig = plt.figure(figsize=(8, 3))                                                        # Definir el tamaño
            graph = sns.set(rc={'axes.facecolor':'#F8F8FF',                                         # Color del fondo
                                'figure.facecolor':'#FFEBC3'})                                      # Color del borde
            graph = sns.scatterplot(x='Sentimiento', y='Valoración', hue='Player', data=df_group)   # Crear gráfica
            graph.set(xscale='linear')                                                              # Definir la escala lineal
            st.pyplot(fig)                                                                          # Pintar en streamlit
        else:
            st.write("""<div class="contenido">No hay datos para la posición seleccionada. """, unsafe_allow_html=True)

'''
#Crear los archivos AHP
model_ahp(stats_file='Stats/Stats_Bases_global.csv', sentiment_file='Stats/Sentiment_Bases.csv', result_file='Model/AHP_Bases.csv')
model_ahp(stats_file='Stats/Stats_Pivots_global.csv', sentiment_file='Stats/Sentiment_Pivots.csv', result_file='Model/AHP_Pivots.csv')
model_ahp(stats_file='Stats/Stats_AlaPivots_global.csv', sentiment_file='Stats/Sentiment_AlaPivots.csv', result_file='Model/AHP_AlaPivots.csv')
model_ahp(stats_file='Stats/Stats_Escoltas_global.csv', sentiment_file='Stats/Sentiment_Escoltas.csv', result_file='Model/AHP_Escoltas.csv')
model_ahp(stats_file='Stats/Stats_Aleros_global.csv', sentiment_file='Stats/Sentiment_Aleros.csv', result_file='Model/AHP_Aleros.csv')
'''