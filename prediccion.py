import pandas as pd
import streamlit as st
from sklearn.model_selection import train_test_split
import numpy as np
from sklearn.ensemble import ExtraTreesRegressor
from sklearn.linear_model import LinearRegression 
from sklearn.svm import SVR
from sklearn import tree
import sklearn.metrics as metrics
import warnings

warnings.filterwarnings("ignore")

def prediction_model(position):
    #Leer el dataframe con la posicion indicada
    csv_file = 'Model/AHP_'+position+'.csv'
    df = pd.read_csv(csv_file)
    df = df.drop(['Game_Day'], axis= 1)
    st.write("Selecciona el jugador y la valoración para realizar la predicción.")

    #Comprobar la posicion de juego y pasar de variable categorica a numerica
    if position == 'Bases':
        df.replace({'Player':{'Nigel Williams-Goss': 0, 'Sergio Llull': 1, 'Juan Nunez': 2, 'Carlos Alocen': 3, 'Thomas Heurtel': 4}}, inplace = True)
        col1, col2 = st.columns([1, 1])
        col1.header("Jugador")
        jugador = col1.selectbox("", ['Nigel Williams-Goss', 'Sergio Llull', 'Juan Nunez', 'Carlos Alocen', 'Thomas Heurtel'], key="selectbox_bases", help="Selecciona un jugador para realizar la predicción.")
        col2.header("Valoración")
        valoracion = col2.slider("", value=0.29 ,min_value=0.0, max_value=1.0, help="Selecciona la valoración del jugador que desea realizar la predicción.")
        if jugador == 'Nigel Williams-Goss':    jugador_prediccion = 0
        if jugador == 'Sergio Llull':           jugador_prediccion = 1
        if jugador == 'Juan Nunez':             jugador_prediccion = 2
        if jugador == 'Carlos Alocen':          jugador_prediccion = 3
        if jugador == 'Thomas Heurtel':         jugador_prediccion = 4

    elif position == 'Aleros':
        df.replace({'Player':{'Rudy Fernandez': 0, 'Alberto Abalde': 1, 'Adam Hanga': 2, 'Fabien Causeur': 3, 'Jeffery Taylor': 4, 'Gabriel Deck': 5}}, inplace = True)
        col1, col2 = st.columns([1, 1])
        col1.header("Jugador")
        jugador = col1.selectbox("", ['Rudy Fernandez', 'Alberto Abalde', 'Adam Hanga', 'Fabien Causeur', 'Jeffery Taylor', 'Gabriel Deck'], key="selectbox_aleros", help="Selecciona un jugador para realizar la predicción.")
        col2.header("Valoración")
        valoracion = col2.slider("", value=0.15 ,min_value=0.0, max_value=1.0, help="Selecciona la valoración del jugador que desea realizar la predicción.")
        if jugador == 'Rudy Fernandez':         jugador_prediccion = 0
        if jugador == 'Alberto Abalde':         jugador_prediccion = 1
        if jugador == 'Adam Hanga':             jugador_prediccion = 2
        if jugador == 'Fabien Causeur':         jugador_prediccion = 3
        if jugador == 'Jeffery Taylor':         jugador_prediccion = 4
        if jugador == 'Gabriel Deck':           jugador_prediccion = 5

    elif position == 'AlaPivots':
        df.replace({'Player':{'Guerschon Yabusele': 0, 'Anthony Randolph': 1, 'Trey Thompkins': 2}}, inplace = True)
        col1, col2 = st.columns([1, 1])
        col1.header("Jugador")
        jugador = col1.selectbox("", ['Guerschon Yabusele', 'Anthony Randolph', 'Trey Thompkins'], key="selectbox_alapivots", help="Selecciona un jugador para realizar la predicción.")
        col2.header("Valoración")
        valoracion = col2.slider("", value=0.15 ,min_value=0.0, max_value=1.0, help="Selecciona la valoración del jugador que desea realizar la predicción.")
        if jugador == 'Guerschon Yabusele':     jugador_prediccion = 0
        if jugador == 'Anthony Randolph':       jugador_prediccion = 1
        if jugador == 'Trey Thompkins':         jugador_prediccion = 2

    elif position == 'Pivots':
        df.replace({'Player':{'Walter Tavares': 0, 'Vincent Poirier': 1}}, inplace = True)
        col1, col2 = st.columns([1, 1])
        col1.header("Jugador")
        jugador = col1.selectbox("", ['Walter Tavares', 'Vincent Poirier'], key="selectbox_Pivots", help="Selecciona un jugador para realizar la predicción.")
        col2.header("Valoración")
        valoracion = col2.slider("", value=0.15 ,min_value=0.0, max_value=1.0, help="Selecciona la valoración del jugador que desea realizar la predicción.")
        if jugador == 'Walter Tavares': jugador_prediccion = 0
        if jugador == 'Vincent Poirier': jugador_prediccion = 1

    #Dividir en valores "feature" y el valor "target"
    X = df.drop(columns='Valoration', axis=1)
    #print('Tabla de valores que se proporcionan: \n', X)
    Y = df['Valoration']
    #print('Tabla del "target" value\n', Y)

    #Dividir datos en Test y Train
    X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, random_state=2)  #If int, random_state is the seed used by the random number generator

    #Modelo
    #Declarar el modelo
    lr_regressor = LinearRegression()
    svr_regressor = SVR()
    dtr_regressor = tree.DecisionTreeRegressor()

    #Entrenar el modelo
    lr_regressor.fit(X_train, Y_train)
    svr_regressor.fit(X_train, Y_train)
    dtr_regressor.fit(X_train, Y_train) #DecisionTreeRegressor
    print('Modelo entrenado.')

    #Model evaluation
    #Prediccion de los datos del Train
    training_data_prediction_lr = lr_regressor.predict(X_train) #Predict Y value
    training_data_regresor_svr = svr_regressor.predict(X_train)
    training_data_regresor_DTreeR = dtr_regressor.predict(X_train)

    #Calculo del Eror de la prediccion
    r2_train_lr = metrics.r2_score(Y_train, training_data_prediction_lr)
    r2_train_svr = metrics.r2_score(Y_train, training_data_regresor_svr)
    r2_train_DecisionTreeRegressor = metrics.r2_score(Y_train, training_data_regresor_DTreeR)
    print('R squared value (LinearRegression)', r2_train_lr)
    print('R squared value (SVR) ', r2_train_svr)
    print('R squared value (DecisionTreeRegressor) ', r2_train_DecisionTreeRegressor)

    #Preparar valores de la prediccion
    print('Predicción: ')
    input_data = (jugador_prediccion, valoracion)
    input_data_np = np.asarray(input_data)  #Pasar a un "numpy" array -> [x1, x2]
    input_data_reshape = input_data_np.reshape(1, -1)   #Reshape array para que este en formato [[x1, x2]] y pasarselo a "predict()"
    print('Se va a realizar la predicción con los datos: ', input_data)

    #Hacer prediccion
    prediction_LR = lr_regressor.predict(input_data_reshape)
    prediction_SVR = svr_regressor.predict(input_data_reshape)
    prediction_DTR = dtr_regressor.predict(input_data_reshape)
    print('Predicción hecha con LinearRegression', prediction_LR)
    print('Predicción hecha con SVR', prediction_SVR)
    print('Predicción hecha con DecisionTreeRegressor', prediction_DTR)
    st.write('La predicción para el jugador **"' + str(jugador) + '"** con una valoración de **"' + str(input_data[1]) + '"** es de **"' + str(prediction_DTR[0]) + '"**.')

def prediction_stats_model(position):
    #Leer el dataframe con la posicion indicada
    csv_file_sentiment = 'Stats/Sentiment_'+position+'.csv'
    csv_file_stats = 'Stats/Stats_'+position+'.csv'
    df_sentiment = pd.read_csv(csv_file_sentiment)
    df_sentiment = df_sentiment.iloc[: , 1:]     #Quitar primera columna
    df_sentiment = df_sentiment.drop(['Game_Day', 'Player'], axis=1)
    df_stats = pd.read_csv(csv_file_stats)
    df_stats = df_stats.iloc[: , 1:]     #Quitar primera columna
    df_stats = df_stats.drop(['Turnovers'], axis=1)
    df_stats['Valoration'] = df_sentiment['Valoration'].values
    st.write("Selecciona el jugador, los puntos, los rebotes, las asistencias, los robos y los tapones para realizar la predicción.")

    #Comprobar la posicion de juego y pasar de variable categorica a numerica
    col1, col2 = st.columns([1, 1])
    if position == 'Bases':
        df_stats.replace({'Player':{'Nigel Williams-Goss': 0, 'Sergio Llull': 1, 'Juan Nunez': 2, 'Carlos Alocen': 3, 'Thomas Heurtel': 4}}, inplace = True)
        print(df_stats)
        col1.header("Jugador")
        jugador = col1.selectbox("", ['Nigel Williams-Goss', 'Sergio Llull', 'Juan Nunez', 'Carlos Alocen', 'Thomas Heurtel'], key="selectbox_bases", help="Selecciona un jugador para realizar la predicción.")
        if jugador == 'Nigel Williams-Goss':    jugador_prediccion = 0
        if jugador == 'Sergio Llull':           jugador_prediccion = 1
        if jugador == 'Juan Nunez':             jugador_prediccion = 2
        if jugador == 'Carlos Alocen':          jugador_prediccion = 3
        if jugador == 'Thomas Heurtel':         jugador_prediccion = 4

    elif position == 'Aleros':
        df_stats.replace({'Player':{'Rudy Fernandez': 0, 'Alberto Abalde': 1, 'Adam Hanga': 2, 'Fabien Causeur': 3, 'Jeffery Taylor': 4, 'Gabriel Deck': 5}}, inplace = True)
        col1.header("Jugador")
        jugador = col1.selectbox("", ['Rudy Fernandez', 'Alberto Abalde', 'Adam Hanga', 'Fabien Causeur', 'Jeffery Taylor', 'Gabriel Deck'], key="selectbox_aleros", help="Selecciona un jugador para realizar la predicción.")
        if jugador == 'Rudy Fernandez':         jugador_prediccion = 0
        if jugador == 'Alberto Abalde':         jugador_prediccion = 1
        if jugador == 'Adam Hanga':             jugador_prediccion = 2
        if jugador == 'Fabien Causeur':         jugador_prediccion = 3
        if jugador == 'Jeffery Taylor':         jugador_prediccion = 4
        if jugador == 'Gabriel Deck':           jugador_prediccion = 5

    elif position == 'AlaPivots':
        df_stats.replace({'Player':{'Guerschon Yabusele': 0, 'Anthony Randolph': 1, 'Trey Thompkins': 2}}, inplace = True)
        col1.header("Jugador")
        jugador = col1.selectbox("", ['Guerschon Yabusele', 'Anthony Randolph', 'Trey Thompkins'], key="selectbox_alapivots", help="Selecciona un jugador para realizar la predicción.")
        if jugador == 'Guerschon Yabusele':     jugador_prediccion = 0
        if jugador == 'Anthony Randolph':       jugador_prediccion = 1
        if jugador == 'Trey Thompkins':         jugador_prediccion = 2

    elif position == 'Pivots':
        df_stats.replace({'Player':{'Walter Tavares': 0, 'Vincent Poirier': 1}}, inplace = True)
        col1.header("Jugador")
        jugador = col1.selectbox("", ['Walter Tavares', 'Vincent Poirier'], key="selectbox_Pivots", help="Selecciona un jugador para realizar la predicción.")
        if jugador == 'Walter Tavares': jugador_prediccion = 0
        if jugador == 'Vincent Poirier': jugador_prediccion = 1

    #Columna 2
    col2.header("Estadísticas")
    puntos = col2.slider("Seleccione los puntos:", value=6 ,min_value=0, max_value=60, help="Selecciona los puntos del jugador que desea realizar la predicción.", key='pts')
    rebotes = col2.slider("Seleccione los rebotes:", value=6 ,min_value=0, max_value=60, help="Selecciona los rebotes del jugador que desea realizar la predicción.", key='rebotes')
    asistencias = col2.slider("Seleccione las asistencias:", value=3 ,min_value=0, max_value=60, help="Selecciona las asistencias del jugador que desea realizar la predicción.", key='asistencias')
    robos = col2.slider("Seleccione los robos:", value=1 ,min_value=0, max_value=60, help="Selecciona los robos del jugador que desea realizar la predicción.", key='robos')
    tapones = col2.slider("Seleccione los tapones:", value=0 ,min_value=0, max_value=60, help="Selecciona los tapones del jugador que desea realizar la predicción.", key='tapones')

    #Dividir en valores "feature" y el valor "target"
    X = df_stats.drop(columns='Valoration', axis=1)
    #print('Tabla de valores que se proporcionan: \n', X)
    Y = df_stats['Valoration']
    #print('Tabla del "target" value\n', Y)

    #Dividir datos en Test y Train
    X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, random_state=2)  #If int, random_state is the seed used by the random number generator

    #Modelo
    #Declarar el modelo
    lr_regressor = LinearRegression()
    svr_regressor = SVR()
    dtr_regressor = tree.DecisionTreeRegressor()

    #Entrenar el modelo
    lr_regressor.fit(X_train, Y_train)
    svr_regressor.fit(X_train, Y_train)
    dtr_regressor.fit(X_train, Y_train) #DecisionTreeRegressor
    print('Modelo entrenado.')

    #Model evaluation
    #Prediccion de los datos del Train
    training_data_prediction_lr = lr_regressor.predict(X_train) #Predict Y value
    training_data_regresor_svr = svr_regressor.predict(X_train)
    training_data_regresor_DTreeR = dtr_regressor.predict(X_train)

    #Calculo del Eror de la prediccion
    r2_train_lr = metrics.r2_score(Y_train, training_data_prediction_lr)
    r2_train_svr = metrics.r2_score(Y_train, training_data_regresor_svr)
    r2_train_DecisionTreeRegressor = metrics.r2_score(Y_train, training_data_regresor_DTreeR)
    print('R squared value (LinearRegression)', r2_train_lr)
    print('R squared value (SVR) ', r2_train_svr)
    print('R squared value (DecisionTreeRegressor) ', r2_train_DecisionTreeRegressor)

    #Prediccion

    #Preparar valores de la prediccion
    print('Predicción: ')
    input_data = (jugador_prediccion, puntos, rebotes, asistencias, robos, tapones)
    input_data_np = np.asarray(input_data)  #Pasar a un "numpy" array -> [x1, x2]
    input_data_reshape = input_data_np.reshape(1, -1)   #Reshape array para que este en formato [[x1, x2]] y pasarselo a "predict()"
    print('Se va a realizar la predicción con los datos: ', input_data)

    #Hacer prediccion
    prediction_LR = lr_regressor.predict(input_data_reshape)
    prediction_SVR = svr_regressor.predict(input_data_reshape)
    prediction_DTR = dtr_regressor.predict(input_data_reshape)
    print('Predicción hecha con LinearRegression', prediction_LR)
    print('Predicción hecha con SVR', prediction_SVR)
    print('Predicción hecha con DecisionTreeRegressor', prediction_DTR)
    col1.write('La predicción para el jugador **"' + str(jugador) + '** con **' + str(puntos) + '** puntos, **' + str(rebotes) + '** rebotes, **' + str(asistencias) + '** asistencias, **' + str(robos) + '** robos y **' + str(tapones) + '** tapones, tiene **"' + str(prediction_DTR[0]) + '"** como valoración de sentimiento.')