import json
import random
import time
import pandas as pd
from drawTeam import drawTeam

from collections import Counter

#Randomly Picks a team

def pickTeam(g,d,m,f):
    gk1 = g[-1] # Cheapest gk, 
    gk2 = random.choice(g)
    while(gk1 == gk2):
        gk2 = random.choice(g)
    
    d1 = random.choice(d)
    d2 = random.choice(d)
    while(d1 == d2):
        d2 = random.choice(d)

    d3 = random.choice(d)
    while(d1 == d3 or d2 == d3):
        d3 = random.choice(d)

    d4 = random.choice(d)
    while(d1 == d4 or d2 == d4 or d3 == d4):
        d4 = random.choice(d)

    d5 = random.choice(d)
    while(d1 == d5 or d2 == d5 or d3 == d5 or d4 == d5):
        d5 = random.choice(d)
        
    m1 = random.choice(m)
    m2 = random.choice(m)
    while(m1 == m2):
        m2 = random.choice(m)

    m3 = random.choice(m)
    while(m1 == m3 or m2 == m3):
        m3 = random.choice(m)

    m4 = random.choice(m)
    while(m1 == m4 or m2 == m4 or m3 == m4):
        m4 = random.choice(m)

    m5 = random.choice(m)
    while(m1 == m5 or m2 == m5 or m3 == m5 or m4 == m5):
        m5 = random.choice(m)

    f1 = random.choice(f)
    f2 = random.choice(f)
    while(f1 == f2):
        f2 = random.choice(f)

    f3 = random.choice(f)
    while(f1 == f3 or f2 == f3):
        f3 = random.choice(f)

    #Sort by points
    defs = sorted([d1,d2,d3,d4,d5],key=lambda k: k['pts'],reverse=True)
    mids = sorted([m1,m2,m3,m4,m5],key=lambda k: k['pts'],reverse=True)
    fwds = sorted([f1,f2,f3],key=lambda k: k['pts'],reverse=True)

    team = [gk1,gk2] + defs + mids + fwds
    if(isLegal(team,1000)):
      return findBestFormation(team)
    else:
        return [0,0,0]
      
    

def isLegal(team,capital):
    price = 0
    teams = []
    for player in team:
        price += player['cost']
        teams.append(player['team'])

    
    if(price > capital):
        return False
    
    ctr = Counter(teams)
    
    #Check if same team is represented more than 3 times
    for k,v in ctr.items():
        if (v > 3):
            return False

    return True

def isLegalDebug(team):
    price = 0
    teams = []
    for player in team:
        price += player['cost']
        teams.append(player['team'])

    print("Price: " + str(price))
    #print('teams: ' + teams)

    if(price > 1000):
        return False

    ctr = Counter(teams)
    
    #CHeck if same team is represented more than 3 times
    for k,v in ctr.items():
        print(v)
        if (v > 3):
            return False
            
    return True

def calculatePoints(team):
    pts = 0
    for p in team:
      pts += float(p['pts'])
    
    return pts
  

def findBestFormation(team):
    g = sorted(list(filter(lambda d: d['pos'] == 'GK', team)),key=lambda k: k['pts'],reverse=True)
    d = sorted(list(filter(lambda d: d['pos'] == 'D', team)),key=lambda k: k['pts'],reverse=True)
    m = sorted(list(filter(lambda d: d['pos'] == 'M', team)),key=lambda k: k['pts'],reverse=True)
    f = sorted(list(filter(lambda d: d['pos'] == 'F', team)),key=lambda k: k['pts'],reverse=True)
    team=g+d+m+f

    points = scoring352(team)
    formation = '3-5-2'

    temp = scoring343(team)
    if(temp > points):
        points = temp
        formation = '3-4-3'
    
    temp = scoring451(team)
    if(temp > points):
        points = temp
        formation = '4-5-1'
    
    temp = scoring442(team)
    if(temp > points):
        points = temp
        formation = '4-4-2'
    
    temp = scoring433(team)
    if(temp > points):
        points = temp
        formation = '4-3-3'

    temp = scoring532(team)
    if(temp > points):
        points = temp
        formation = '5-3-2'
    
    temp = scoring541(team)
    if(temp > points):
        points = temp
        formation = '5-4-1'
    
    return [team,points,formation]

"""
    Formations
    3-4-3
    3-5-2
    4-5-1
    4-4-2
    4-3-3
    5-4-1
    5-3-2
"""

def scoring352(team):
    temp = [team[0],team[2],team[3],team[4],team[7],team[8],team[9],team[10],team[11],team[12],team[13]]
    return calculatePoints(temp)

def scoring343(team):
    temp = [team[0],team[2],team[3],team[4],team[7],team[8],team[9],team[10],team[12],team[13],team[14]]
    return calculatePoints(temp)
def scoring451(team):
    temp = [team[0],team[2],team[3],team[4],team[5],team[7],team[8],team[9],team[10],team[11],team[12]]
    return calculatePoints(temp)
def scoring442(team):
    temp = [team[0],team[2],team[3],team[4],team[5],team[7],team[8],team[9],team[10],team[12],team[13]]
    return calculatePoints(temp)
def scoring433(team):
    temp = [team[0],team[2],team[3],team[4],team[5],team[7],team[8],team[9],team[12],team[13],team[14]]
    return calculatePoints(temp)
def scoring541(team):
    temp = [team[0],team[2],team[3],team[4],team[5],team[6],team[7],team[8],team[9],team[10],team[12]]
    return calculatePoints(temp)
def scoring532(team):
    temp = [team[0],team[2],team[3],team[4],team[5],team[6],team[7],team[8],team[9],team[12],team[13]]
    return calculatePoints(temp)


def buildSquad(attempts,source):
    with open('data/projections/' + source +  '.json','r') as fpl:
        all_players = json.load(fpl)

    #fill player positions
    gks = list(filter(lambda d: d['pos'] == 'GK', all_players))
    defs = list(filter(lambda d: d['pos'] == 'D', all_players))
    mids = list(filter(lambda d: d['pos'] == 'M', all_players))
    fwds = list(filter(lambda d: d['pos'] == 'F', all_players))

    counter = 0

    best_team = []
    best_points = 0
    best_formation = ''
    start = time.time()
    print("run simulation")

    while(counter < attempts):
        if not(counter % 100000):
            print(counter / attempts)
        counter += 1
        team = pickTeam(gks,defs,mids,fwds)
        if(team[1] > best_points):
            best_team = team[0]
            best_points = team[1]
            best_formation = team[2]
    end = time.time()

    print('Finished ' + str(attempts) + ' in ' + str((end - start)) + ' seconds') 
    print('------------')
    print('------------')
    print(best_points)
    print('------------')
    print(best_formation)
    print('------------')

    drawTeam(best_formation,best_team,'pre_suggest',[])
    return best_team

def getGKAndHandcuff(gk,gks):
    print("finding gk handcuff")
    gks = list(filter(lambda d: d['team'] == gk['team'], gks))
    return gks[0:2]

def buildSmartSquad(attempts,source):
    with open('data/projections/' + source +  '.json','r') as fpl:
        all_players = json.load(fpl)

    jsonTocsv = pd.read_json('data/projections/' + source +  '.json')
    jsonTocsv.to_csv('data/projections/' + source +  '.csv',index=False)

    #fill player positions
    gks = list(filter(lambda d: d['pos'] == 'GK', all_players))
    defs = list(filter(lambda d: d['pos'] == 'D', all_players))
    mids = list(filter(lambda d: d['pos'] == 'M', all_players))
    fwds = list(filter(lambda d: d['pos'] == 'F', all_players))

    gks = sorted(gks,key=lambda k: k['ppp'],reverse=True)
    defs = sorted(defs,key=lambda k: k['ppp'],reverse=True)
    mids = sorted(mids,key=lambda k: k['ppp'],reverse=True)
    fwds = sorted(fwds,key=lambda k: k['ppp'],reverse=True)

    counter = 0

    start = time.time()
    print("run simulation")
    team = getGKAndHandcuff(gks[0],gks)+defs[0:5]+mids[0:5]+fwds[0:3]
    #print(team)
    
    if(isLegal(team,1000)):
        team = findBestFormation(team)
        drawTeam(team[2],team[0],'smart_suggest',[])
        
    else:
        print("not legal")

    
    posMap = {
        'GK':gks,
        'D':defs,
        'M':mids,
        'F':fwds
    }
    team = team[0]
    replacementIndex = 0
    while(counter < attempts):
        print("-------------"+str(replacementIndex)+"----------loop-----"+str(counter)+"-----------------")
        #print(team)
        counter += 1
        #find lowest performer
        print("find lowest performer")
        weakestLink = sorted(team[2:],key=lambda k: k['pts'],reverse=True)[replacementIndex]
        print(weakestLink)

        #find next replacement
        replacement = next((obj for obj in posMap[weakestLink['pos']] if obj['pts'] > weakestLink['pts'] and obj not in team),-1)
        if(replacement == -1):
            print("no replacement found")
            replacementIndex += 1
            if replacementIndex > 12:
                replacementIndex = 0
        else:
            print(team.index(weakestLink))
            print(replacement)
            
            team[team.index(weakestLink)] = replacement

            if(isLegal(team,1000)):
                team = findBestFormation(team)
                drawTeam(team[2],team[0],'v4_smart_suggest_'+ str(counter),[])
                team = team[0]
            else:
                team[team.index(replacement)] = weakestLink
                replacementIndex += 1
                if replacementIndex > 12:
                    replacementIndex = 0
        
    
    return team



#buildSquad(100)
