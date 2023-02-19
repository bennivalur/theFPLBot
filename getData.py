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
        if(getNextGameWeek() < 6):
            myobj = {'season': '2022','league':'epl'}
        else:
            myobj = {'season': '2022','league':'epl','date_start':getRangeStart(5)}

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

    jsonTocsv = pd.read_json('tempfiles/fpl_players.json')
    jsonTocsv.to_csv('tempfiles/fpl_players.csv',index=False)
  
def getLeague(league):
    fpl = urllib.request.urlopen("https://fantasy.premierleague.com/api/leagues-classic/"+ str(league) + "/standings/").read()
    fpl = json.loads(fpl)

    
    with open('tempfiles/botsvsbots.json','r') as main_pl:
        entries = json.load(main_pl)


    if(entries != []):
        if(entries[-1]["last_updated_data"] != fpl['last_updated_data']):
            entries.append(fpl)
        
            with open('tempfiles/botsvsbots.json', 'w') as file:
                file.write(json.dumps(entries))
    else:
        with open('tempfiles/botsvsbots.json', 'w') as file:
                file.write(json.dumps([fpl]))

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

    main_table.rename(columns={'team_x':'team'},inplace=True)

    fpl.to_csv('tempfiles/pl_all_players.csv',index=False)
    unders.to_csv('tempfiles/under_all_players.csv',index=False)

    main_table.to_csv('tempfiles/maindata.csv',index=False)
    main_table.to_json('tempfiles/maindata.json',orient='records')

    keys.to_json('keys_pl_understat.json',orient='records')

def findMissingPlayers():
    with open('tempfiles/fpl_players.json','r') as fpl:
        all_players = json.load(fpl)
    
    with open('keys_pl_understat.json','r') as main_pl:
        keys = json.load(main_pl)
    for k in keys:
        if(k['understat_id'] != None):
            k['understat_id'] = round(k['understat_id'])
        if(k['fpl_id'] != None):
            k['fpl_id'] = round(k['fpl_id'])
    missingPL = []
    for p in all_players:
        if(next((x for x in keys if x['fpl_id'] == p['id']), None) == None):
            missingPL.append(p)
    with open('tempfiles/understat.json','r') as fpl:
        all_players = json.load(fpl)
    
    missingUnder = []
    for p in all_players:
        if(next((x for x in keys if str(x['understat_id']) == str(p['id'])), None) == None):
            missingUnder.append(p)

    with open('tempfiles/missing_pl.json', 'w') as file:
        file.write(json.dumps(missingPL))

    with open('tempfiles/missing_under.json', 'w') as file:
        file.write(json.dumps(missingUnder))

    fpl = pd.read_json('tempfiles/missing_pl.json')
    unders = pd.read_json('tempfiles/missing_under.json')
    fpl.to_csv('tempfiles/missing_fpl.csv',index=False)
    unders.to_csv('tempfiles/missing_under.csv',index=False)

def plAllToJson():
    print("pl_all_players to json")
    cs = pd.read_csv('tempfiles/pl_all_players.csv')
    cs.to_json('tempfiles/pl_all_players.json',orient='records')
    
def getFixtures(week):
    print("Get FPL Fixtures")
    games = urllib.request.urlopen("https://fantasy.premierleague.com/api/fixtures/").read()
    games = json.loads(games)
    games = list(filter(lambda g: g['event'] == week, games))

    with open('tempfiles/fixtures.json', 'w') as file:
        file.write(json.dumps(games))


def getData(week):
    getSeasons('EPL','2022')
    getFPL()
    getUnderStat()
    mergeSets()
    getFixtures(week)
    plAllToJson()


#week = 26
#getData(week)
