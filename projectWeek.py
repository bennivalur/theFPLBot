from projectionScoring import *
from configTeams import *
from timeFunctions import *
import json
from scoring import *


def makeWeeklyProjections(week):
    with open('dataMergingFiles/maindata.json','r') as main_pl:
        main_players = json.load(main_pl)
    
    #Project each player
    player_projections = []
    isPreseason = False
    for p in main_players:
        player_projections.append(scoring(p,isPreseason))
        
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
    
    with open('data/projections/' + getCurrentSeasonStartYear() + '_' +  str(int(getCurrentSeasonStartYear())+1 ) + '/week_' + str(week) + '.json', 'w') as file:
        file.write(json.dumps(player_projections))
    print("Projections Made")
    print("weekly projections")