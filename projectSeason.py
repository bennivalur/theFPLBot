from projectionScoring import *
from configTeams import *
from timeFunctions import *
import json


def makeSeasonProjections():
    with open('dataMergingFiles/maindata.json','r') as main_pl:
        main_players = json.load(main_pl)
    
    #Project each player
    player_projections = []
    for p in main_players:
        player_projections.append(scoring(p))
        
    #Sort players by projected points
    player_projections = sorted(player_projections, key=lambda x: x['pts'],reverse=True)

    #Rank by position
    i = {
        'GK':0,
        'D':0,
        'M':0,
        'F':0
    }
    for pl in player_projections:
        #print(positions[p['element_type']])
        pl['rank'] = i[pl['pos']]
        i[pl['pos']] += 1
    
    with open('data/projections/' + getCurrentSeasonStartYear() + '_' +  str(int(getCurrentSeasonStartYear())+1 ) + '_preseason.json', 'w') as file:
        file.write(json.dumps(player_projections))
    print("Projections Made")

    



def scoring(p):
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

        pts += p['bonus']

        #Goals, assists, yellows
        pts += goals_scoring[pos] * (goals + xg) / 2
        pts += assists_scoring[pos] * (assists + xa) / 2
        pts += yellows * -1

        #if GK
        if(pos == 1):
            pts += p['saves'] * gk_scoring['saves']
            pts += p['penalties_saved'] * gk_scoring['penalties_saved']

        

        if(minutes/games >= 60):
            pts += 2 *games
        elif (minutes/games > 10):
            pts += games


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