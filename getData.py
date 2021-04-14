import asyncio
import json
import pandas as pd
import os
import urllib.request
import aiohttp
from datetime import datetime
from getLeagueResults import getSeasons
from predictCS import getRangeStart,getNextGameWeek
import requests
from understat import Understat

async def main():
    async with aiohttp.ClientSession() as session:
        url = 'https://understat.com/main/getPlayersStats/'
        myobj = {'season': '2020','league':'epl','date_start':getRangeStart(5)}

        players = requests.post(url, data = myobj)
        players = players.json()
        players = players['response']['players']
        players = json.dumps(players)
        with open('tempfiles/understat.json', 'w') as file:
            file.write(players)
        
def getFPL():
    print("Get FPL")
    fpl = urllib.request.urlopen("https://fantasy.premierleague.com/api/bootstrap-static/").read()
    fpl = json.loads(fpl)
    fpl_players = fpl['elements']

    _events = fpl['events']
    _events = json.dumps(_events)
    with open('tempfiles/events.json', 'w') as file:
        file.write(_events)

    with open('tempfiles/fpl_players.json', 'w') as file:
        file.write(json.dumps(fpl_players))
  

def getUnderStat():
    print("Get Understat")
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())


def mergeSets():
    print("Merge Datasets")
    fpl = pd.read_json('tempfiles/fpl_players.json')
    unders = pd.read_json('tempfiles/understat.json')

    fpl.rename(columns={'id': 'fpl_id'}, inplace=True)
    unders.rename(columns={'id':'understat_id'},inplace=True)

    keys = pd.read_csv('keys_pl_understat.csv', low_memory=False)

    main_table = pd.merge(fpl,keys, on='fpl_id',how='inner')
    main_table = pd.merge(main_table,unders, on='understat_id',how='inner')
    #main_table = pd.merge(main_table,pos, on='fpl_id',how='inner')

    #player_teams = pd.merge(keys,unders,on='understat_id', how='inner')
    #player_teams.to_csv('teamshelper.csv',index=False)

    fpl.to_csv('tempfiles/pl_all_players.csv',index=False)
    unders.to_csv('tempfiles/under_all_players.csv',index=False)

    main_table.to_csv('tempfiles/maindata.csv',index=False)
    main_table.to_json('tempfiles/maindata.json',orient='records')

def plAllToJson():
    print("pl_all_players to json")
    cs = pd.read_csv('tempfiles/pl_all_players.csv')
    cs.to_json('tempfiles/pl_all_players.json',orient='records')
    
def getFixtures(week):
    print("Get FPL Fixtures")
    games = urllib.request.urlopen("https://fantasy.premierleague.com/api/fixtures/").read()
    games = json.loads(games)
    games = list(filter(lambda g: g['event'] == week+1, games))

    with open('tempfiles/fixtures.json', 'w') as file:
        file.write(json.dumps(games))


def getData(week):
    getSeasons('EPL','2020')
    getFPL()
    getUnderStat()
    mergeSets()
    getFixtures(week)
    plAllToJson()


#week = 26
#getData(week)