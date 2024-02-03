import asyncio
import json
import urllib.request
import aiohttp
from datetime import datetime

import pandas as pd

from understat import Understat

from getData import fplFixtures, getRangeStart,getNextGameWeek, getGameWeek, getFix


teams = [
    {'title':'0','uid':-1},
    {'title':'Arsenal','uid': '83'},
    {'title':'Aston Villa','uid':'71'},
    {'title':'Bournemouth','uid':'-1'},
    {'title':'Brentford','uid':'244'},
    {'title':'Brighton','uid':'220'},
    {'title':'Burnley','uid':'-1'},
    {'title':'Chelsea', 'uid':'80'},
    {'title':'Crystal Palace','uid':'78'},
    {'title':'Everton','uid':'72'},
    {'title':'Fulham','uid':'-1'},
    {'title':'Liverpool','uid':'87'},
    {'title':'Luton Town','uid':'-1'},
    {'title':'Manchester City','uid':'88'},
    {'title':'Manchester United','uid':'89'},
    {'title':'Newcastle United','uid':'86'},
    {'title':'Nottingham Forest','uid':'-1'},
    {'title':'Sheffield United','uid':'-1'},
    {'title':'Tottenham','uid':'82'},
    {'title':'West Ham', 'uid':'81'},
    {'title':'Wolverhampton Wanderers','uid':'229'},
    {'title': 'Luton','uid':'-1'},
]

async def getFixtures(season):
    async with aiohttp.ClientSession() as session:
        understat = Understat(session)
        results = await understat.get_league_fixtures(
            "epl", season
        )

        data = json.dumps(results)
        with open('tempfiles/unders_fixtures.json', 'w') as file:
            file.write(data)

def getUnderStat(season):
    loop = asyncio.get_event_loop()
    loop.run_until_complete(getFixtures(season))


def getResults():
    with open('tempfiles/EPL_2023_res.json', 'r') as all_weeks:
        results = json.load(all_weeks)
    return results
    

def calcOdds(xGSum):
    odds = (xGSum * -1 * 0.103044) + 0.564388
    if odds <= 0:
        return 0
    return odds

def calcWinOdds(xGSum):
    odds = (xGSum  * 0.116178) + 0.392198
    if odds <= 0:
        return 0
    return odds


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


#getUnderStat(2020)
def predictCS():
    print("Predicting Clean Sheets Odds")
    getUnderStat('2023')
    fplFixtures(False)
    week = getNextGameWeek() - 1

    deadline = getGameWeek(week)['deadline_time']
    print(f'Deadline: {deadline}')
    endOfGameWeek = getGameWeek(week+1)['deadline_time']

    #Get upcoming fixtures
    games = getFix()
    games = sorted(games, key=lambda t: datetime.strptime(t['kickoff_time'], '%Y-%m-%dT%H:%M:%SZ'))

    #Filter games in upcoming gameweek
    gameweekGames = []
    for g in games:
        if(g['kickoff_time'] < endOfGameWeek and g['kickoff_time'] > deadline):
            gameweekGames.append([teams[g['team_h']],teams[g['team_a']],{'code':g['code']}])
        
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

        homeWinOdds = round(calcWinOdds((homeXG['xG']+awayXG['xGA']) - (awayXG['xG']+homeXG['xGA'])),2)
        awayWinOdds = round(calcWinOdds((awayXG['xG']+homeXG['xGA']) - (homeXG['xG']+awayXG['xGA'])),2)

        allOdds.append({'team':g[0]['title'],'opponent':g[1]['title'],'csOdds':homeOdds,'winOdds':homeWinOdds,'code':g[2]['code']})
        allOdds.append({'team':g[1]['title'],'opponent':g[0]['title'],'csOdds':awayOdds,'winOdds':awayWinOdds,'code':g[2]['code']})

    with open('tempfiles/clean_sheet_odds.json', 'w') as file:
        file.write(json.dumps(allOdds))



