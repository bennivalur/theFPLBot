import json
import urllib.request
import aiohttp
import pandas as pd
import asyncio
import requests
from understat import Understat

def getFPLPlayerAndMatchData():
    print("Get FPL Player and Match Data...")
    fpl = urllib.request.urlopen("https://fantasy.premierleague.com/api/bootstrap-static/").read()
    fpl = json.loads(fpl)
    fpl_players = fpl['elements']

    _events = fpl['events']
    _events = json.dumps(_events)
    with open('data/matchData/events.json', 'w') as file:
        file.write(_events)

    with open('data/playerData/fpl_players.json', 'w') as file:
        file.write(json.dumps(fpl_players))

    jsonTocsv = pd.read_json('data/playerData/fpl_players.json')
    jsonTocsv.to_csv('data/playerData/fpl_players.csv',index=False)

def getFPLPlayerHistory():
    with open('data/playerData/fpl_players.json','r') as fpl:
        all_players = json.load(fpl)

    for p in all_players:
        fpl = urllib.request.urlopen("https://fantasy.premierleague.com/api/element-summary/" + str(p['id']) + "/").read()
        fpl = json.loads(fpl)
        
        with open('data/historicFPLData/'+ p['web_name'] + '_' + str(p['id']) + '.json', 'w') as file:
            file.write(json.dumps(fpl['history_past']))
   
        print(p['web_name'])

async def main(season):
    async with aiohttp.ClientSession() as session:
        url = 'https://understat.com/main/getPlayersStats/'
        #if(getNextGameWeek() < 6):
        print(season)
        print("season")
        myobj = season
        print(myobj)
        #else:
        #    myobj = {'season': season,'league':'epl','date_start':getRangeStart(5)}

        players = requests.post(url, data = myobj)
        players = players.json()
        players = players['response']['players']
        players = json.dumps(players)
        with open('data/historicalUnderstatData/'+ season['season'] +'.json', 'w') as file:
            file.write(players)

def getUnderstatPlayers():
    print("Get Understat")
    season = {'season': "2024",'league':'epl'}
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(season))

def getUnderstatPlayerHistory():
    print("Get Understat")
    season = {'season': "2023",'league':'epl'}
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(season))

