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
from statistics import mean
import numpy as np

import matplotlib.pyplot as plt
from matplotlib.offsetbox import OffsetImage, AnnotationBbox



from getData import *

async def main():
    async with aiohttp.ClientSession() as session:
        url = 'https://understat.com/main/getPlayersStats/'
        myobj = {'season': '2022','league':'epl'}

        players = requests.post(url, data = myobj)
        players = players.json()
        players = players['response']['players']
        players = json.dumps(players)
        with open('tempfiles/understat2023.json', 'w') as file:
            file.write(players)

        
        main_table = pd.read_json('tempfiles/understat2023.json')
        main_table.to_csv('tempfiles/understat2023.csv',index=False)

def getUnderStat():
    print("Get Understat")
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())



        

#GetData
def gData():
    getSeasons('EPL','2022')
    getFPL()
    getUnderStat()
    mergeSets()
    plAllToJson()


teams = [
    '0',
    'Arsenal',
    'Aston Villa',
    'Bournemouth',
    'Brentford',
    'Brighton',
    'Burnley',
    'Chelsea',
    'Crystal Palace',
    'Everton',
    'Fulham',
    'Liverpool',
    'Luton',
    'Man City',
    'Man Utd',
    'Newcastle',
    'Nott\'m Forest',
    'Sheffield Utd',
    'Spurs',
    'West Ham',
    'Wolves'
]
teams_u = [
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
]

colors = {
    'Arsenal':'#EF0107',
    'Aston Villa':'#95BFE5',
    'Brighton':'#005daa',
    'Bournemouth':'#DA291C',
    'Brentford':'#e30613',
    'Burnley':'#6C1D45',
    'Chelsea':'#034694',
    'Crystal Palace':'#1b458f',
    'Everton':'#274488',
    'Fulham':'#ffffff',
    'Liverpool':'#d01317',
    'Luton':'#FFFFFF',
    'Man City':'#6CADDF',
    'Man Utd':'#da020e',
    'Newcastle':'#000000',
    'Nott\'m Forest':"#e53233",
    'Sheffield Utd':'#EE2737',
    'Spurs':'#ffffff',
    'West Ham':'#7c2c3b',
    'Wolves':'#FDB913',
}


positions = [
    '0',
    'GK',
    'D',
    'M',
    'F',
]
#Clean Sheets
#Points for clean sheets by position
cs = [
    0,
    4,
    4,
    1,
    0
]
#Goals
#Points for goals by positions
goals_scoring = [
    0,
    6,
    6,
    5,
    4
]
#Assists
#Points for goals by positions
assists_scoring = [
    0,
    3,
    3,
    3,
    3
]

gk_scoring = {
    'saves':0.33,
    'penalties_saved':5
}



def makeProjections():

    with open('tempfiles/fpl_players.json','r') as fpl:
        all_players = json.load(fpl)

    with open('tempfiles/maindata.json','r') as main_pl:
        main_players = json.load(main_pl)
    
    


    player_projections = []
    for p in all_players:
        player = list(filter(lambda pl: pl['fpl_id'] == p['id'], main_players))
        if(player != []):
            
            player_projections.append(scoring(player[0]))
        else:
            pl = {
                'name':p['first_name'] + ' ' + p['second_name'],
                'pts':0,
                'ppp':0,
                'team':teams[p['team']],
                'color':colors[teams[p['team']]],
                'pos':positions[p['element_type']],
                'cost':p['now_cost'],
                'short':p['web_name'],
                'fpl_id':p['id'],
                'rank':0
            }
            player_projections.append(pl)
            
            
    player_projections = sorted(player_projections, key=lambda x: x['pts'],reverse=True)

    i = {
        'GK':0,
        'D':0,
        'M':0,
        'F':0
    }
    #Position Rank
    for pl in player_projections:
        #print(positions[p['element_type']])
        pl['rank'] = i[pl['pos']]
        i[pl['pos']] += 1
    
    with open('tempfiles/projections.json', 'w') as file:
        file.write(json.dumps(player_projections))
    print("Projections Made")

    
def chanceHelper(chance_of_playing):
    if(chance_of_playing == None):
        return 1
    else:
        return chance_of_playing / 100


def scoring(p):
    print(p)
    pos = p['element_type']
    team = p['team']

    games = p['games']

    
    
    pts = 0
    if(games != 0):
        goals = p['goals']
        xg = p['xG']

        assists = p['assists_y']
        xa = p['xA']

        yellows = p['yellow_cards_x']

        minutes = p['time']

        pts += goals_scoring[pos] * (goals + xg) / 2
        pts += assists_scoring[pos] * (assists + xa) / 2
        pts += yellows * -1

        #if GK
        if(pos == 1):
            saves = p['saves'] 
            pts += saves * gk_scoring['saves']
            penalties = p['penalties_saved']
            pts += penalties * gk_scoring['penalties_saved']

        predictedMinutes = predictMinutes(p['web_name_x'],p['fpl_id'])

        pts = (pts / minutes) * predictedMinutes

        playingPoints = (predictedMinutes / 60) * 2

        pts += playingPoints

        print(p['web_name_x'] + " last minutes: " + str(minutes) + " | predicted minutes: " + str(predictedMinutes))

    
    pl = {
        'name':p['player_name_x'],
        'pts':round(pts,2),
        'ppp':pts/((p['now_cost']/10)),
        'team':teams[team],
        'color':colors[teams[team]],
        'pos':positions[pos],
        'cost':p['now_cost'],
        'short':p['web_name_x'],
        'fpl_id':p['fpl_id'],
        'rank':0
    }
    
    return pl

#Use carefully, lol
def getHistory():
    with open('tempfiles/fpl_players.json','r') as fpl:
        all_players = json.load(fpl)

    for p in all_players:
        fpl = urllib.request.urlopen("https://fantasy.premierleague.com/api/element-summary/" + str(p['id']) + "/").read()
        fpl = json.loads(fpl)
        
        with open('playerHistory/'+ p['web_name'] + '_' + str(p['id']) + '.json', 'w') as file:
            file.write(json.dumps(fpl))
   
        print(p['web_name'])

def best_fit_slope_and_intercept(xs,ys):
    m = (((mean(xs)*mean(ys)) - mean(xs*ys)) /
         ((mean(xs)*mean(xs)) - mean(xs*xs)))
    
    b = mean(ys) - m*mean(xs)
    
    return m, b

def predictMinutes(name,id):
    with open('playerHistory/'+ name + '_' + str(id) + '.json','r') as fpl:
        player = json.load(fpl)
    
    player = player['history_past']

    if(len(player) > 5):
        player = player[5:]

    if(len(player) > 1):
        x = []
        minutes = []
        index = 1
        for s in player:
            x.append(index)
            minutes.append(s['minutes'])
            index += 1


        xs = np.array(x, dtype=np.float64)
        ys = np.array(minutes, dtype=np.float64)

        m, b = best_fit_slope_and_intercept(xs,ys)

        predicted_minutes = (m*index)+b 
    elif (len(player) == 1):
        predicted_minutes = player[0]['minutes']
    else:
        print(name + " zero seasons" )
        predicted_minutes = 0

    if(predicted_minutes < 0):
        predicted_minutes = 0
    elif(predicted_minutes > 3420):
        predicted_minutes = 3420

    return predicted_minutes



    



#predictMinutes('Kane',357)
#plotProjections('Kane',357)
#plotTop(4)


getSeasons('EPL','2022')
getFPL()
getUnderStat()
mergeSets()
plAllToJson()

#Use Carefully
getHistory()

makeProjections()