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
    {'title':'Brentford','uid':'244'},
    {'title':'Brighton','uid':'220'},
    {'title':'Bournemouth','uid':'-1'},
    {'title':'Chelsea', 'uid':'80'},
    {'title':'Crystal Palace','uid':'78'},
    {'title':'Everton','uid':'72'},
    {'title':'Leicester','uid':'75'},
    {'title':'Leeds','uid':'245'},
    {'title':'Liverpool','uid':'87'},
    {'title':'Manchester City','uid':'88'},
    {'title':'Manchester United','uid':'89'},
    {'title':'Newcastle United','uid':'86'},
    {'title':'Nottingham Forest','uid':'-1'},
    {'title':'Southampton', 'uid':'74'},
    {'title':'Tottenham','uid':'82'},
    {'title':'Fulham','uid':'-1'},
    {'title':'West Ham', 'uid':'81'},
    {'title':'Wolverhampton Wanderers','uid':'229'},
]

lengjan_teams = {
    'Arsenal':'Arsenal',
    'Aston Villa':'Aston Villa',
    'Brentford':'Brentford',
    'Brighton':'Brighton',
    'Burnley':'Burnley',
    'Chelsea':'Chelsea',
    'Crystal Palace':'Crystal Palace', # not confirmed
    'Everton':'Everton', #not confirmed
    'Leicester':'Leicester', # not confirmed
    'Leeds':'Leeds',
    'Liverpool':'Liverpool',
    'Man.City':'Manchester City',
    'Man.Utd.':'Manchester United',
    'Newcastle':'Newcastle United',
    'Norwich':'Norwich',
    'Southampton':'Southampton',
    'Tottenham':'Tottenham',
    'Watford':'Watford',
    'West Ham':'West Ham',
    'Wolves':'Wolverhampton Wanderers',
    'Fulham':'Fulham',# not confirmed
    'Brentford':'Brentford', # not confirmed
    'Nott.Forest':'Nottingham Forest',
    'Bournemouth':'Bournemouth'
}

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

def fplFixtures(isAllSeason):
    fpl = urllib.request.urlopen("https://fantasy.premierleague.com/api/fixtures/").read()
    fpl = json.loads(fpl)
    if not isAllSeason:
        fixtures = [x for x in fpl if x['finished'] == False and x['kickoff_time'] != None]
        results = json.dumps(fixtures)
        with open('tempfiles/fixtures.json', 'w') as file:
            file.write(results)
    else:
        results = json.dumps(fpl)
        with open('tempfiles/all_fpl_fixtures.json', 'w') as file:
            file.write(results)

def getResults():
    with open('tempfiles/EPL_2021_res.json', 'r') as all_weeks:
        results = json.load(all_weeks)
    return results
    

def calcOdds(xGSum):
    #odds = (xGSum * -1 * 0.103044) + 0.564388
    #New formula as of 18.02.2023
    odds = (xGSum * -1 * 0.112397) + 0.589429
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
    
    return games[week]


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
    getUnderStat('2022')
    fplFixtures(False)
    week = getNextGameWeek() - 1

    deadline = getGameWeek(week)['deadline_time']
    print(deadline)
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

        allOdds.append({'team':g[0]['title'],'opponent':g[1]['title'],'csOdds':homeOdds,'code':g[2]['code']})
        allOdds.append({'team':g[1]['title'],'opponent':g[0]['title'],'csOdds':awayOdds,'code':g[2]['code']})

    with open('tempfiles/clean_sheet_odds.json', 'w') as file:
        file.write(json.dumps(allOdds))

def checkBetResults(bet_amount,odds_margin):
    #fplFixtures(True)
    print("chekking bet results")
    
    with open('tempfiles/bet_scheme.json', 'r') as all_bets:
        bets = json.load(all_bets)

    with open('tempfiles/all_fpl_fixtures.json', 'r') as file:
        results = json.load(file)
    wins = 0
    losses = 0
    balance = 0
    for b in bets:
        if((float(b['myOdds']) - float(b['lengjanOdds'])) > odds_margin):
            g = next(item for item in results if item["code"] == b['fpl_code'])
            if(g['finished']):
                if(b['home_away'] == 'home'):
                    if(b['cS'] == 'Yes'):
                        if(g['team_a_score'] > 0):
                            balance -= bet_amount
                            losses += 1
                        else:
                            balance += bet_amount * (1/float(b['lengjanOdds']))
                            wins += 1
                    else:
                        if(g['team_a_score'] == 0):
                            balance += bet_amount * (1/float(b['lengjanOdds']))
                            wins += 1
                        else:
                            balance -= bet_amount
                            losses += 1
                else:
                    if(b['cS'] == 'Yes'):
                        if(g['team_h_score'] > 0):
                            balance -= bet_amount
                            losses += 1
                        else:
                            balance += bet_amount * (1/float(b['lengjanOdds']))
                            wins += 1
                    else:
                        if(g['team_h_score'] == 0):
                            balance += bet_amount * (1/float(b['lengjanOdds']))
                            wins += 1
                        else:
                            balance -= bet_amount
                            losses += 1

    print("wins: " + str(wins))
    print("losses: " + str(losses))            
    print("balance: " + str(balance))
    percentProf = balance /((wins + losses)*bet_amount + balance) * 100
    #percentProf = balance / starting_budget * 100
    print(str(round(percentProf,2)) + '%')

def checkBets():
    print("Checking Bets")
    with open('tempfiles/clean_sheet_odds.json', 'r') as all_games:
        games = json.load(all_games)


    odds = urllib.request.urlopen("https://games.lotto.is/game/lengjan-events?live=0").read()
    odds = json.loads(odds)

    events = odds['events']
    pl_events = []
    for e in events:
        if e['compid'] == '296':
            #print(e['participants'])
            pl_events.append(e)


    markets = {}

    for e in pl_events:
        odds = urllib.request.urlopen("https://games.lotto.is/game/lengjan-markets?live=0&eventId=" + str(e['eventid'])).read()
        odds = json.loads(odds)
        odds = odds['markets']
        markets[e['eventid']] = {}
        markets[e['eventid']]['markets'] = []
        markets[e['eventid']]['participants'] = e['participants']
        markets[e['eventid']]['understat'] = []
        for g in games:
            if(e['participants'][0]['name'][-1] == ' '):
                if g['team'] == lengjan_teams[e['participants'][0]['name'][:-1]]:
                    markets[e['eventid']]['understat'].append(g)
            else: 
                if g['team'] == lengjan_teams[e['participants'][0]['name']]:
                    markets[e['eventid']]['understat'].append(g)

            if(e['participants'][1]['name'][-1] == ' '):
                if g['team'] == lengjan_teams[e['participants'][1]['name'][:-1]]:
                    markets[e['eventid']]['understat'].append(g)
            else: 
                if g['team'] == lengjan_teams[e['participants'][1]['name']]:
                    markets[e['eventid']]['understat'].append(g)


        for o in odds:
            if o['marketsubtype'] == '44' or o['marketsubtype'] == '43':
                markets[e['eventid']]['markets'].append({'marketname':o['marketname'],'selections':o['selections']})
    
    

    with open('tempfiles/temp_clean_sheet_odds.json', 'w') as file:
        file.write(json.dumps(markets))

    with open('tempfiles/bet_scheme.json', 'r') as all_games:
        bets_to_save = json.load(all_games)

    for key in markets:
        home_team = markets[key]['understat'][0]['team']
        my_home_team_odds = str(markets[key]['understat'][0]['csOdds'])
        lengjan_home_team_odds = str(100 / float(markets[key]['markets'][0]['selections'][1]['odds']))

        my_home_concede_odds = str(1.0 - float(my_home_team_odds))
        lengjan_home_team_concede_odds = str(100 / float(markets[key]['markets'][0]['selections'][0]['odds']))


        away_team = markets[key]['understat'][1]['team']
        my_away_team_odds = str(markets[key]['understat'][1]['csOdds'])
        lengjan_away_team_odds = str(100 / float(markets[key]['markets'][1]['selections'][1]['odds']))

        my_away_concede_odds = str(1.0 - float(my_away_team_odds))
        lengjan_away_team_concede_odds = str(100 / float(markets[key]['markets'][1]['selections'][0]['odds']))

        #Print out and save entries if our models odds are morer favorable than the odds of Lengjan
        if(float(my_home_team_odds) > float(lengjan_home_team_odds)):
            print('BET Clean Sheet(+' + str(round(100*(float(my_home_team_odds) - float(lengjan_home_team_odds)),2)) + '%): ' + home_team + ' against ' + away_team + ': ' + my_home_team_odds+ ' ' + lengjan_home_team_odds)
            bets_to_save.append({'cS':'Yes','home_away':'home','team':home_team,'opponent':away_team,'myOdds':my_home_team_odds,'lengjanOdds':lengjan_home_team_odds,'fpl_code':markets[key]['understat'][0]['code'],'result':0})
        if((float(my_home_concede_odds) > float(lengjan_home_team_concede_odds))):
            print('BET NO Clean Sheet(+' + str(round(100*(float(my_home_concede_odds) - float(lengjan_home_team_concede_odds)),2))+ '%): ' + home_team + ' against ' + away_team + ': ' + my_home_concede_odds + ' ' + lengjan_home_team_concede_odds)
            bets_to_save.append({'cS':'No','home_away':'home','team':home_team,'opponent':away_team,'myOdds':my_home_concede_odds,'lengjanOdds':lengjan_home_team_concede_odds,'fpl_code':markets[key]['understat'][0]['code'],'result':0})
        if(float(my_away_team_odds) > float(lengjan_away_team_odds)):
            print('BET Clean Sheet(+' + str(round(100*(float(my_away_team_odds) - float(lengjan_away_team_odds)),2)) + '%): ' + away_team + ' against ' + home_team + ': ' + my_away_team_odds+ ' ' + lengjan_away_team_odds)
            bets_to_save.append({'cS':'Yes','home_away':'away','team':away_team,'opponent':home_team,'myOdds':my_away_team_odds,'lengjanOdds':lengjan_away_team_odds,'fpl_code':markets[key]['understat'][0]['code'],'result':0})
        if((float(my_away_concede_odds) > float(lengjan_away_team_concede_odds))):
            print('BET NO Clean Sheet(+' + str(round(100*(float(my_away_concede_odds) - float(lengjan_away_team_concede_odds)),2))+ '%): ' + away_team + ' against ' + home_team + ': ' + my_away_concede_odds + ' ' + lengjan_away_team_concede_odds)
            bets_to_save.append({'cS':'No','home_away':'away','team':away_team,'opponent':home_team,'myOdds':my_away_concede_odds,'lengjanOdds':lengjan_away_team_concede_odds,'fpl_code':markets[key]['understat'][0]['code'],'result':0})

        with open('tempfiles/bet_scheme.json', 'w') as file:
            file.write(json.dumps(bets_to_save))
        #print(home_team + ' against ' + away_team + ': ' + my_home_team_odds+ ' ' + lengjan_home_team_odds + ' | ' +  my_home_concede_odds + ' ' + lengjan_home_team_concede_odds)
        #print(away_team + ' against ' + home_team + ': ' + my_away_team_odds+ ' ' + lengjan_away_team_odds + ' | ' +  my_away_concede_odds + ' ' + lengjan_away_team_concede_odds)
        
    #for b in bets_to_save:
    #    print(b)



#predictCS()
