from fpl import findBestFormation,isLegal
import copy
import json,urllib
import itertools

def getTeam(team_id,week):
    try:
        with urllib.request.urlopen("https://fantasy.premierleague.com/api/entry/"+ str(team_id) +"/event/"+ str(week) +"/picks/") as url:
            data = json.loads(url.read().decode())
            if(type(data) is dict):
                return data
            else:
                return 'error'
    except:
        return 'error'

def convertFPLteam(team):
    squad = []
    with open('tempfiles/projections.json','r') as fpl:
        all_players = json.load(fpl)
    for p in team:
        squad.append((next((x for x in all_players if x['fpl_id'] == p['element']), None)))

    squad = list(filter(lambda d: d['pos'] == 'GK', squad)) + list(filter(lambda d: d['pos'] == 'D', squad)) + list(filter(lambda d: d['pos'] == 'M', squad)) +list(filter(lambda d: d['pos'] == 'F', squad))

    return squad

#Players in team
#Number of free transfers (1,2)
def suggestTransfers(players,free_transfers,capital):
    with open('tempfiles/projections.json','r') as fpl:
        all_players = json.load(fpl)

    players_sorted = {
        'GK': list(filter(lambda d: d['pos'] == 'GK', all_players)),
        'D' : list(filter(lambda d: d['pos'] == 'D', all_players)),
        'M' : list(filter(lambda d: d['pos'] == 'M', all_players)),
        'F' : list(filter(lambda d: d['pos'] == 'F', all_players))
    }

    temp = findBestFormation(players)
    current_pts = temp[1]
    print("Current team best points: " + str(current_pts))

    transfer_suggestions = []
    for index, p in enumerate(players):
        for tr in players_sorted[p['pos']]:
            if p != tr and tr not in players:
                temp_team = copy.deepcopy(players)
                temp_team[index] = tr
                if(isLegal(temp_team,capital)):
                    
                    transfer_suggestions.append(temp_team)

    best_pts = current_pts
    take_hit = False

    for t in transfer_suggestions:
        temp = findBestFormation(t)
        if(temp[1] > best_pts):
            if(temp[1] + 4 > best_pts):
                take_hit = True
            best_pts = temp[1]
            best_formation = temp[2]
            best_team = temp[0]
    
    many_transfers = 0
    while(free_transfers > many_transfers):
        many_transfers += 1
    if(not many_transfers):
        take_hit = False
        for index, p in enumerate(best_team):
            for tr in players_sorted[p['pos']]:
                if p != tr and tr not in best_team:
                    temp_team = copy.deepcopy(best_team)
                    temp_team[index] = tr
                    if(isLegal(temp_team,capital)):
                        transfer_suggestions.append(temp_team)

        best_pts = 0
        for t in transfer_suggestions:
            temp = findBestFormation(t)
            if(temp[1] > best_pts and isLegal(temp[0],capital)):
                if(temp[1] + 4 > best_pts):
                    take_hit = True
                best_pts = temp[1]
                best_formation = temp[2]
                best_team = temp[0]
    

    transfered_players = list(itertools.filterfalse(lambda x: x in players, best_team)) + list(itertools.filterfalse(lambda x: x in best_team, players))
    
    return [best_formation,best_team,transfered_players]
    
    



   
    
