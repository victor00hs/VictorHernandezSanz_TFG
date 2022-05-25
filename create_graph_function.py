import json
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
 
''' Function that creates a graph from total.json values '''
def sentiment_graph(data):
  #Read file
  with open(data, 'r') as file:
    data_set = json.load(file)

  #Create dataframe with the JSON
  df = pd.DataFrame(data_set)

  #Take day
  data_day = data[:-11]  # Removes last 11characters to have "data_YYYY-MM-DD"
  day = data_day[-10:]    # Takes last 10 digits "YYYY-MM-DD"
  title_graph = "Análisis de sentimiento de jugadores del "+ day

  #Create graph
  df.plot.scatter(x="Player", y="Valoration", c="Valoration", colormap="jet") # "c" is used as the variable "colormap" will take to apply a color dependiong with the numerical value
  plt.xticks(rotation=90)                                                     # Set X-axis names vertical
  plt.subplots_adjust(top=0.94, right=0.96, bottom=0.4)                       # Adjust size of the graph
  plt.grid(color='r', linestyle='--', linewidth=0.1)                          # "color"-> red, "linestyle"-> dashed line, "linewidth"-> size of the line
  plt.title(title_graph)
  plt.xlabel("Jugadores")
  plt.ylabel("Valoración")
  plt.show()

''' Streamlit function '''
def sentiment_graph_streamlit(data):
    #Read file
    with open(data, 'r') as file:
        data_set = json.load(file)

    #Create dataframe with the JSON
    df = pd.DataFrame(data_set)

    #Take day
    data_day = data[:-11]  # Removes last 11characters to have "data_YYYY-MM-DD"
    day = data_day[-10:]    # Takes last 10 digits "YYYY-MM-DD"

    #Streamlit text
    st.write("""<h1 class="titulo-h1"> Representación del sentimiento de los jugadores para el partido del día """ + str(day), unsafe_allow_html=True)
    st.write("""<p class="contenido">A continuación se muestra una gráfica que representa a los <strong>jugadores</strong>, frente a la <strong>valoración</strong> de los tweets que han escrito los usuarios en twitter 
                comprendida entre -1 y 1, recogida del partido que tuvo lugar el día """ + "<strong>" + str(day) + "</strong>.", unsafe_allow_html=True)
    
    title_graph = "Análisis de sentimiento de jugadores del "+ day
    x_axis = df["Player"]           # Define x axis
    y_axis = df["Valoration"]       # Define y axis
    color_var = y_axis              # Define varable for the color (has to be a number)
    color_range = "jet"              # Define de color the graph will take depending on the value ("jet", "viridis"...)
    #Create graph
    width = 10
    height = 3.6
    fig = plt.figure(figsize=(width, height))
    plt.scatter(x=x_axis, y=y_axis, c=color_var, cmap=color_range)        
    plt.xticks(rotation=90)                                                     # Set X-axis names vertical
    plt.subplots_adjust(top=0.94, right=0.96, bottom=0.4)                       # Adjust size of the graph
    plt.grid(color='r', linestyle='--', linewidth=0.1)                          # "color"-> red, "linestyle"-> dashed line, "linewidth"-> size of the line
    plt.title(title_graph)
    plt.xlabel("Jugadores")
    plt.ylabel("Valoración")
    plt.colorbar()
    
    #Print graph
    with st.spinner("Espere unos segundos..."):     #In case it takes too much time, it will show a spinner loading
      st.pyplot(fig)

    #Data table
    st.write("En caso de que se quiera ver con precisión el valor de los datos, también se muestra una tabla con todos los valores recogidos para este día:")
    st.dataframe(data=df, width=500, height=600)


#MAIN
if __name__ == "__main__":
  data = 'data_2022-04-03/total.json'
  sentiment_graph(data)