from projectionScoring import *
from configTeams import *
from timeFunctions import *
import json
from statistics import mean
import numpy as np

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

        finishing_rate = calculateFinishingRating(p['understat'])

        #Goals, assists, yellows
        pts += goals_scoring[pos] *  xg * finishing_rate
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

    projected_minutes = predictMinutes(p['understat'])


    if minutes != 0:
        factor = projected_minutes/minutes
        if factor > 1.2:
            factor = 1.2
        elif factor < 0.8:
            factor = 0.8
        pts = pts * factor
        projected_minutes = minutes * factor

    if p['chance_of_playing_next_round'] == 0.0:
        pts = 0

    pl = {
        'name':p['player_name'],
        'pts':round(pts,2),
        'ppp':pts/((p['now_cost']/10)),
        'team':teams[team],
        'color':colors[teams[team]],
        'pos':positions[pos],
        'cost':p['now_cost'],
        'short':p['web_name_x'],
        'fpl_id':p['fpl_id'],
        'code':p['code'],
        'rank':0,
        'minutes_last_season':minutes,
        'minutes_projected':projected_minutes
    }
    return pl

def calculateFinishingRating(understat_id):
    with open('data/historicalUnderstatData/'+ str(int(float(understat_id))) + '.json','r') as history:
        history = json.load(history)
    totalXG = 0
    totalGoals = 0
    for season in history:
        totalXG += float(season['xG'])
        totalGoals += float(season['goals'])

    if totalXG != 0:
        return totalGoals/totalXG
    else:
        return 0

def predictMinutes(understat_id):
    with open('data/historicalUnderstatData/'+ str(int(float(understat_id))) + '.json','r') as history:
        history = json.load(history)
    
    if(len(history) > 5):
        history = history[5:]

    if(len(history) > 1):
        x = []
        minutes = []
        index = 1
        for s in history:
            x.append(index)
            minutes.append(s['time'])
            index += 1


        xs = np.array(x, dtype=np.float64)
        ys = np.array(minutes, dtype=np.float64)

        m, b = best_fit_slope_and_intercept(xs,ys)

        predicted_minutes = float((m*index)+b )
    elif (len(history) == 1):
        predicted_minutes = float(history[0]['time'])
    else:
        predicted_minutes = 0

    if(predicted_minutes < 0):
        predicted_minutes = 0
    elif(predicted_minutes > 3420):
        predicted_minutes = 3420

    return predicted_minutes

def best_fit_slope_and_intercept(xs,ys):
    m = (((mean(xs)*mean(ys)) - mean(xs*ys)) /
         ((mean(xs)*mean(xs)) - mean(xs*xs)))
    
    b = mean(ys) - m*mean(xs)
    
    return m, b