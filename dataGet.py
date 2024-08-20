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
        myobj = season
        #else:
        #    myobj = {'season': season,'league':'epl','date_start':getRangeStart(5)}

        players = requests.post(url, data = myobj)
        players = players.json()
        players = players['response']['players']
        players = json.dumps(players)
        with open('data/playerData/understat_players.json', 'w') as file:
            file.write(players)

async def getPLayerGroupedStats(id):
   
    async with aiohttp.ClientSession() as session:
        understat = Understat(session)
        grouped_stats = await understat.get_player_grouped_stats(id)
        grouped_stats = grouped_stats['season']
        grouped_stats = json.dumps(grouped_stats)
        
            
        #print(grouped_stats)
        
        with open('data/historicalUnderstatData/'+ str(id) +'.json', 'w') as file:
            file.write(grouped_stats)

def getHistoricUnderstatData():

    with open('dataMergingFiles/maindata.json','r') as fpl:
        all_players = json.load(fpl)

    for p in all_players:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(getPLayerGroupedStats(int(float(p['understat']))))

def getHistoricUnderstatDataByID(understatID):
    loop = asyncio.get_event_loop()
    loop.run_until_complete(getPLayerGroupedStats(understatID))


def getUnderstatPlayers(season):
    print("Get Understat")
    season = {'season': str(season),'league':'epl'}
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(season))


def getNextGameWeek():
    fpl = urllib.request.urlopen("https://fantasy.premierleague.com/api/bootstrap-static/").read()
    fpl = json.loads(fpl)
    fpl_players = fpl['elements']

    _events = fpl['events']
    
    for e in _events:
        if(e['is_next']):
            return e['id']
