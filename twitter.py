import os
import json
from tweepy import OAuthHandler, API, Cursor
from textblob import TextBlob
from deep_translator import GoogleTranslator
from datetime import timedelta, datetime

# Tokens for the OAuthHandler
consumer_api_key = 'LQnuQFTcCO1b18621kH7mPTga'
consumer_api_key_secret = 'cjYlQgWL3aebS1lHb6RqKOYJnByPtamamuZykwMyEWmJNzN0uT' 
access_token = '1673748180-g6RuQgGkM4FX4ugnb9JCPSbTY3hu0vUlQwaHvcH'
access_token_secret = 'PNLypKIWoFEbm60X6NyknVGfM8BLTqKdzLd7loCv8zMvm'

# We set the connection to the tweepy API
auth = OAuthHandler(consumer_api_key, consumer_api_key_secret)
auth.set_access_token(access_token, access_token_secret)
api = API(auth)

def scrape_search_tweets(query, num_tweets):
    output = []
    info_array = []
    total_json = {}
    total_sentiment = 0.0
    
    for i, tweet in enumerate(Cursor(api.search_tweets, q=query, lang='es', result_type='mixed', tweet_mode = 'extended').items(num_tweets)):       #tweet_mode -> instead of tweet.text (only some characters) using tweet.full_text
        if i > num_tweets:
            break
        try:
            to_translate = tweet.full_text                                                      #Take full text of tweet 
            translated = GoogleTranslator(source='auto', target='en').translate(to_translate)   #Translate to english
            sentimiento = TextBlob(translated).sentiment                                        #Apply sentiment analysis
            sentimiento = round(sentimiento.polarity, 2)                                        #Take "polarity" value and round it with 2decimals
        except Exception as e:
            sentimiento = 0.0                                                                   #In case it doesn't take a value, default as 0.0
        total_sentiment = total_sentiment + sentimiento                                         #Increment "total_sentiment"
        #Append all Twitter data into "info_array"
        info_array.append({
            'Tweet_No': str(i+1),
            'Basketball_Player': player_names[countador-1],
            'Date': str(tweet.created_at),
            'ID': tweet.id_str,
            'Content': tweet.full_text,
            'Username': tweet.user.name,
            'Sentiment': sentimiento
        })

    #Append all data into "output"
    output.append({
        'Info': info_array,                                                                             #All info from Twitter + sentiment
        'Total_valoration': 0 if 0 == len(info_array) else round(total_sentiment/len(info_array), 3),   #If "len(info_array) = 0" it sets a 0 (avoid mistakes) else it does the sentiment average
        'Basketball_Player': player_names[countador-1],                                                 #Player name
        'Game_Day': days[game_day-1]                                                                    #Day of the game
    })
    json_output = json.dumps(output, indent=4)
    
    #Add "json_output" information for individual players
    #Create a directory of the game day if not exists and save data
    try:
        os.makedirs("./data_" + str(days[game_day-1]))
        with open("./data_" + str(days[game_day-1]) + "/player_" + player_names[countador-1] + ".json", "w") as outfile:
            outfile.write(json_output)
    #Directory already exists, so it will only save data
    except FileExistsError:
        with open("./data_" + str(days[game_day-1]) + "/player_" + player_names[countador-1] + ".json", "w") as outfile:
            outfile.write(json_output)
    
    #Add "total_json" information for a single file
    #Write 'name', 'valoration' and 'day' to a JSON
    total_json.update({
        'Player': player_names[countador-1],
        'Valoration': 0 if 0 == len(info_array) else round(total_sentiment/len(info_array), 3),  #If len(info_array) = 0 set value 0 (avoid errors) else do average
        'Game_Day': days[game_day-1]})
    with open("./data_" + str(days[game_day-1]) + "/total.json", 'a+') as json_file:
        json.dump(total_json, json_file, indent=4)
        json_file.write(",\n")

    return json.dumps(output, indent=4, ensure_ascii=False)


# MAIN
if __name__ == "__main__":
    #Players chosen to do data extraction
    player_names = ['Nigel Williams-Goss', 'Juan Nuñez',                #2
                    'Thomas Heurtel', 'Carlos Alocen', 'Llull',          #5
                    'Carroll', 'Causeur', 'Rudy Fernandez',             #8
                    'Alberto Abalde', 'Adam Hanga', 'Gabriel Deck',     #11
                    'Jeffery Taylor', 'Anthony Randolph', 'Vukcevic',   #14
                    'Yabusele', 'Trey Thompkins', 'Vincent Poirier',    #17
                    'Tavares', 'Pablo Laso',                            #19     #Laso -> entrenador
                    'Urban Klavzar', 'Baba Miller', 'Sediq Garuba']     #22     Urban Klavzar, Baba Miller, Sediq Garuba -> canterano (jugó bien el 23/12)

    #Days done: 5, 6, 7, 8, 10, 11, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47
    #Days miss: 9, 12, 13, 
    game_day = 47
    tweets = 70
    rated_players = 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15 ,16, 17, 18, 19 #Todos
        
    #Game days: 33, 41        34, 42       35,43           36            37              38           39             40
    days = ['2021-12-02', '2021-12-04', '2021-12-10', '2021-12-12', '2021-12-14', '2021-12-16', '2021-12-19', '2021-12-23', 
            '2022-01-04', '2022-01-09', '2022-01-14', '2022-01-16', '2022-01-20', '2022-01-23', '2022-01-25', '2022-01-28',
            '2022-01-30', '2022-02-02', '2022-02-04', '2022-02-06', '2022-02-08', '2022-02-11', '2022-02-13', '2022-02-17',
            '2022-02-19', '2022-02-20', '2022-02-24', '2022-03-06', '2022-03-08', '2022-03-10', '2022-03-13', '2022-03-17',
            '2022-03-20', '2022-03-22', '2022-03-24', '2022-03-27', '2022-03-31', '2022-04-03', '2022-04-08', '2022-04-10',
            '2022-04-13', '2022-04-17', '2022-04-20', '2022-04-22', '2022-04-24', '2022-04-26', '2022-05-01']
    
    #Day after game auxiliar
    days_after = []

    #Taking next day of match day
    count = 0
    for i in days:
        datetime_object = datetime.strptime(days[count], '%Y-%m-%d')    #Convert to day
        day_after = datetime_object + timedelta(days=1)                 #Add 1 day
        day_after = day_after.strftime('%Y-%m-%d')                      #Format
        days_after.append(day_after)                                    #Add to list
        count = count+1
    
    ''' scrape_search_tweets '''
    for countador in rated_players:
        scrape_search_tweets(player_names[countador-1] + ' since:' + days[game_day-1] + ' until:' + days_after[game_day-1], tweets)