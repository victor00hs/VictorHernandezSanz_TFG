import json
from pymongo import MongoClient
import os

def add_mongodb_players(path, collection_name):
  print("Inicio add_mongodb_players")
  #Connect to the cluster
  client = MongoClient('mongodb+srv://Victor00hs:Mirabal2000@clusterv.a663e.mongodb.net/myFirstDatabase?retryWrites=true&w=majority')
  #Connect to the database
  db = client.get_database('Twitter')
  #Connect to the collection (In case it does not exists, create it)
  records = db[collection_name]
  #Check number of documents in the collection selected
  print("Antes de insertar, había " + str(records.count_documents({})) + " documentos en la colección: " + str(collection_name))
  player_files = []
  index = 0
  #Add to mongo
  for i in os.listdir(path):                                        #Take all files in "path"
      if os.path.isfile(os.path.join(path,i)) and 'player_' in i:   #If the "path/player_" append it to "files"
          player_files.append(i)
          print(player_files[index])
          with open(path + "/" + str(player_files[index])) as file: #Open al JSONs with the player data and load it to "data"
            data = json.load(file)
          print(data)
          records.insert_many(data)                                 #Add information with "insert_many()"
          index = 1+index                                           #Increase the value of index
  print("Despues de insertar, hay " + str(records.count_documents({})) + " documentos en la colección " + str(collection_name))
  print("Fin add_mongodb_players")



def add_mongodb_total(path, collection_name):
  print("Inicio add_mongodb_total")
  full_path = path + "/total.json"
  #Connect to the cluster
  client = MongoClient('mongodb+srv://Victor00hs:Mirabal2000@clusterv.a663e.mongodb.net/myFirstDatabase?retryWrites=true&w=majority')
  #Connect to the database
  db = client.get_database('Twitter')
  #Connect to the collection (In case it does not exists, create it)
  records = db[collection_name]
  #Check number of documents in the collection selected
  print("Antes de insertar, había " + str(records.count_documents({})) + " documentos en la colección: " + str(collection_name))
  #Add to mongo
  with open(full_path) as file:     #Open al JSONs with the player data and load it to "data"
    data = json.load(file)
  records.insert_many(data)         #Add information with "insert_many()"
  print("Despues de insertar, hay " + str(records.count_documents({})) + " documentos en la colección " + str(collection_name))
  print("Fin add_mongodb_total")

if __name__ == "__main__":
    path = 'data_2022-05-01'                                        #Folder path (in python.py you can find an array with all possible values)
    if(len(path) == 15):                                            #Check if the path has 15 characters in case its wrong spelled
      collection_name_jugadores = path[-10:]                        #Take "yyyy-mm-dd" Last 10 characters
      collection_name_total = collection_name_jugadores + "_total"  #Modify name of the name of the collection
      add_mongodb_players(path, collection_name=collection_name_jugadores)
      add_mongodb_total(path, collection_name=collection_name_total)
    else:
      print("No se han llamado a las funciones add_mongodb_players() ni add_mongodb_total().")