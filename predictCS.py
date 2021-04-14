import asyncio
import json
import os
import urllib.request
import aiohttp
from datetime import datetime

import pandas as pd

from understat import Understat


teams = [
    {'title':'0','uid':-1},
    {'title':'Arsenal','uid': '83'},
    {'title':'Aston Villa','uid':'71'},
    {'title':'Brighton','uid':'220'},
    {'title':'Burnley','uid':'92'},
    {'title':'Chelsea', 'uid':'80'},
    {'title':'Crystal Palace','uid':'78'},
    {'title':'Everton','uid':'72'},
    {'title':'Fulham','uid':'228'},
    {'title':'Leicester','uid':'75'},
    {'title':'Leeds','uid':'245'},
    {'title':'Liverpool','uid':'87'},
    {'title':'Manchester City','uid':'88'},
    {'title':'Manchester United','uid':'89'},
    {'title':'Newcastle United','uid':'86'},
    {'title':'Sheffield United', 'uid':'238'},
    {'title':'Southampton', 'uid':'74'},
    {'title':'Tottenham','uid':'82'},
    {'title':'West Bromwich Albion','uid':'76'},
    {'title':'West Ham', 'uid':'81'},
    {'title':'Wolverhampton Wanderers','uid':'229'},
]
async def getFixtures(season):
    async with aiohttp.ClientSession() as session:
        understat = Understat(session)
        results = await understat.get_league_fixtures(
            "epl", season
        )

        data = json.dumps(results)
        with open('tempfiles/fixtures.json', 'w') as file:
            file.write(data)

def getUnderStat(season):
    loop = asyncio.get_event_loop()
    loop.run_until_complete(getFixtures(season))

def fplFixtures():
    fpl = urllib.request.urlopen("https://fantasy.premierleague.com/api/fixtures/").read()
    fpl = json.loads(fpl)
    fixtures = [x for x in fpl if x['finished'] == False and x['kickoff_time'] != None]
    results = json.dumps(fixtures)
    with open('tempfiles/fixtures.json', 'w') as file:
        file.write(results)

def getResults():
    with open('tempfiles/EPL_2020_res.json', 'r') as all_weeks:
        results = json.load(all_weeks)
    return results
    

def calcOdds(xGSum):
    odds = (xGSum * -1 * 0.103044) + 0.564388
    if odds <= 0:
        return 0
    return odds

def getNextGameWeek():
    with open('tempfiles/events.json', 'r') as all_weeks:
        weeks = json.load(all_weeks)
    
    for e in weeks:
        if(e['is_next']):
            return e['id']

def getGameWeek(week):
    with open('tempfiles/events.json', 'r') as all_games:
        games = json.load(all_games)
    
    return games[week-1]


def getFix():
    with open('tempfiles/fixtures.json', 'r') as all_games:
        games = json.load(all_games)
    
    return games

def calcXG(games,teamID):
    xG = 0
    xGA = 0

    for tg in games:
        if(tg['h']['id'] == teamID):
            team = 'h'
            opponent = 'a'
        else:
            team = 'a'
            opponent = 'h'

        xG += float(tg['xG'][team])
        xGA += float(tg['xG'][opponent])
    
    xG = xG/5
    xGA = xGA/5
    return {'xG':xG,'xGA':xGA}

def getRangeStart(form_range):
    week = getNextGameWeek()

    return getGameWeek(week-form_range)['deadline_time']

#getUnderStat(2020)
def predictCS():
    print("Predicting Clean Sheets Odds")
    fplFixtures()
    week = getNextGameWeek()

    deadline = getGameWeek(week)['deadline_time']
    endOfGameWeek = getGameWeek(week+1)['deadline_time']

    #Get upcoming fixtures
    games = getFix()
    games = sorted(games, key=lambda t: datetime.strptime(t['kickoff_time'], '%Y-%m-%dT%H:%M:%SZ'))

    #Filter games in upcoming gameweek
    gameweekGames = []
    for g in games:
        if(g['kickoff_time'] < endOfGameWeek and g['kickoff_time'] > deadline):
            gameweekGames.append([teams[g['team_h']],teams[g['team_a']]])
        
    #Get games already played
    results = getResults()

    allOdds = []

    for g in gameweekGames:
        #Get last 5 games a team player in
        homeTeamGames = [x for x in results if x['h']['id'] == g[0]['uid'] or x['a']['id'] == g[0]['uid']][-5:]
        awayTeamGames = [x for x in results if x['h']['id'] == g[1]['uid'] or x['a']['id'] == g[1]['uid']][-5:]

        #Calculate xg
        homeXG = calcXG(homeTeamGames,g[0]['uid'])
        awayXG = calcXG(awayTeamGames,g[1]['uid'])

        #Calculate odds
        homeOdds = round(calcOdds(awayXG['xG']+homeXG['xGA']),2)
        awayOdds = round(calcOdds(homeXG['xG']+awayXG['xGA']),2)

        allOdds.append({'team':g[0]['title'],'opponent':g[1]['title'],'csOdds':homeOdds})
        allOdds.append({'team':g[1]['title'],'opponent':g[0]['title'],'csOdds':awayOdds})


    with open('tempfiles/clean_sheet_odds.json', 'w') as file:
        file.write(json.dumps(allOdds))

#predictCS()
