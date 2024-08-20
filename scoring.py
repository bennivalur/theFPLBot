from projectionScoring import *
from configTeams import *
from timeFunctions import *
import json
from statistics import mean
import numpy as np
from dataGet import getHistoricUnderstatDataByID

def scoring(p,isPreseason):
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

        

        

    projected_minutes = predictMinutes(p['understat'])

    if minutes != 0:
        factor = projected_minutes/minutes
        if factor > 1.1:
            factor = 1.1
        elif factor < 0.9:
            factor = 0.9
        pts = pts * factor
        projected_minutes = minutes * factor
    
    if not isPreseason:
        if projected_minutes > 90:
            projected_minutes = 90

    if(projected_minutes/games >= 60):
        pts += 2 *games
    elif (projected_minutes/games > 10):
        pts += games
    #Clean sheets
    cs = estimateCleanSheetsPerGame(p['fpl_id'],p['web_name_x'])
    cs = round(cs * projected_minutes,2)

    #Times conceded more than 2
    goals_conceded_per_game = p['goals_conceded']/(games-cs)
    goals_conceded_minus = 0
    if goals_conceded_per_game > 2:
        goals_conceded_minus = -1*(goals_conceded_per_game-2)*(games-cs)

    pts += cs * clean_sheets[pos]
    
    if pos in [1,2]:
        pts += goals_conceded_minus

    if p['chance_of_playing_next_round'] == 0.0:
        pts = 0

    pl = {
        'name':p['player_name'],
        'pts':round(pts,2),
        'ppp':round(pts/((p['now_cost']/10)),2),
        'team':teams[team],
        'color':colors[teams[team]],
        'pos':positions[pos],
        'cost':p['now_cost'],
        'short':p['web_name_x'],
        'fpl_id':p['fpl_id'],
        'code':p['code'],
        'rank':0,
        'minutes_last':minutes,
        'minutes_projected':projected_minutes,
        'clean_sheets':cs,
        'goals_conceded_minus':round(goals_conceded_minus)
    }
    return pl

def calculateFinishingRating(understat_id):
    try:
        with open('data/historicalUnderstatData/'+ str(int(float(understat_id))) + '.json','r') as history:
            history = json.load(history)
    except:
        getHistoricUnderstatDataByID(understat_id)
        """with open('data/historicalUnderstatData/'+ str(int(float(understat_id))) + '.json','r') as history:
            history = json.load(history)"""

    totalXG = 0
    totalGoals = 0
    for season in history:
        totalXG += float(season['xG'])
        totalGoals += float(season['goals'])

    if totalXG != 0:
        return totalGoals/totalXG
    else:
        return 0
    
def estimateCleanSheetsPerGame(fpl_id,web_name):
    with open('data/historicFPLData/'+ web_name + '_' + str(fpl_id) + '.json','r') as history:
        history = json.load(history)
    totalCleanSheets = 0
    totalMinutes = 0
    for season in history:
        totalCleanSheets += float(season['clean_sheets'])
        totalMinutes += float(season['minutes'])

    if totalMinutes != 0:
        return totalCleanSheets/totalMinutes
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