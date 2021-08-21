import urllib.request
import pandas as pd
import json

#from understat import Understat
from getData import getData

teams = [
    '0',
    'Arsenal',
    'Aston Villa',
    'Brentford',
    'Brighton',
    'Burnley',
    'Chelsea',
    'Crystal Palace',
    'Everton',
    'Leicester',
    'Leeds',
    'Liverpool',
    'Man City',
    'Man Utd',
    'Newcastle',
    'Norwich',
    'Southampton',
    'Spurs',
    'Watford',
    'West Ham',
    'Wolves'
]
teams_u = [
    {'title':'0','uid':-1},
    {'title':'Arsenal','uid': '83'},
    {'title':'Aston Villa','uid':'71'},
    {'title':'Brentford','uid':'244'},
    {'title':'Brighton','uid':'220'},
    {'title':'Burnley','uid':'92'},
    {'title':'Chelsea', 'uid':'80'},
    {'title':'Crystal Palace','uid':'78'},
    {'title':'Everton','uid':'72'},
    {'title':'Leicester','uid':'75'},
    {'title':'Leeds','uid':'245'},
    {'title':'Liverpool','uid':'87'},
    {'title':'Manchester City','uid':'88'},
    {'title':'Manchester United','uid':'89'},
    {'title':'Newcastle United','uid':'86'},
    {'title':'Norwich','uid':'79'},
    {'title':'Southampton', 'uid':'74'},
    {'title':'Tottenham','uid':'82'},
    {'title':'Watford','uid':'90'},
    {'title':'West Ham', 'uid':'81'},
    {'title':'Wolverhampton Wanderers','uid':'229'},
]

colors = {
    'Arsenal':'#EF0107',
    'Aston Villa':'#95BFE5',
    'Brighton':'#005daa',
    'Burnley':'#6C1D45',
    'Brentford':'#e30613',
    'Chelsea':'#034694',
    'Crystal Palace':'#1b458f',
    'Everton':'#274488',
    'Leeds':'#ffffff',
    'Leicester':'#0053a0',
    'Liverpool':'#d01317',
    'Man City':'#6CADDF',
    'Man Utd':'#da020e',
    'Newcastle':'#000000',
    'Norwich':"#00A650",
    'Southampton':'#D71920',
    'Spurs':'#ffffff',
    'Watford':'#fbee23',
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
    
    with open('tempfiles/clean_sheet_odds.json','r') as cs:
        clean_sheets = json.load(cs)


    player_projections = []
    for p in all_players:
        player = list(filter(lambda pl: pl['fpl_id'] == p['id'], main_players))
        if(player != []):
            odds = {
                'clean_sheet':list(filter(lambda x: x['team'] == teams_u[player[0]['team']]['title'] ,clean_sheets ))
            }
            player_projections.append(scoring(player[0],odds))
        else:
            pl = {
                'name':p['first_name'] + ' ' + p['second_name'],
                'pts':0,
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


def scoring(p,odds):
    pos = p['element_type']
    team = p['team']

    games = p['games']

    if(p['points_per_game'] != 0):
        total_games = p['total_points'] / p['points_per_game']
    else:
        total_games = 1
    
    
    pts = 0
    if(games != 0) and odds['clean_sheet'] != None:
        goals = p['goals']
        xg = p['xG']

        assists = p['assists_y']
        xa = p['xA']

        yellows = p['yellow_cards_x'] / total_games

        minutes = p['time']

        pts += goals_scoring[pos] * (goals + xg) / 2
        pts += assists_scoring[pos] * (assists + xa) / 2
        pts += yellows * -1

        cH = chanceHelper(p['chance_of_playing_next_round'])
        #if GK
        if(pos == 1):
            saves = p['saves'] / total_games
            pts += saves * gk_scoring['saves']
            penalties = p['penalties_saved'] / total_games
            pts += penalties * gk_scoring['penalties_saved']

        pts = pts / games

        if(minutes/games >= 60):
            pts += 2
        elif (minutes/games > 10):
            pts += 1

        pts = pts * cH * len(odds['clean_sheet'])

        for o in odds['clean_sheet']:
            pts += cs[pos] * float(o['csOdds'])


    pl = {
        'name':p['player_name'],
        'pts':round(pts,2),
        'team':teams[team],
        'color':colors[teams[team]],
        'pos':positions[pos],
        'cost':p['now_cost'],
        'short':p['web_name'],
        'fpl_id':p['fpl_id'],
        'rank':0
    }
    return pl



#makeProjections()