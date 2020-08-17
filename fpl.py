import pandas as pd
import os
import urllib.request
import json
import random
import operator
import time

from collections import Counter

with open('fpl.json') as f_in:
       players = json.load(f_in)

#Creates puts the fpl and understat data together
#Some records don't match up and should be edited in whatver csv editor to improve the data before running
def makeMain():
    understat = pd.read_csv('understat2020.csv', low_memory=False)
    pl = pd.read_csv('pl2020.csv', low_memory=False)

    data = pd.merge(understat,pl,on='full_name',how='inner')

    with open('main_table.csv', 'w') as file:
            file.write(data.to_csv(index=False))

    players = pd.read_csv('main_table.csv', low_memory=False)

    players.to_json ('fpl.json',orient='records', lines=True)

#Get players from certain position: G D M F
def fillPlayers(players,position):
    return list(filter(lambda d: d['pos_y'] == position, players))

def gkScoring(players):
    pl = {}
    gks = []
    for p in players:
      xga = ((p['xG'] * 6) + ((p['xA']) * 3))
      cs = ((p['clean_sheets']) * 4)
      gc = ((p['goals_conceded']) * -0.5)
      saves = ((p['saves']  ) / 3)
      pens = ((p['penalties_saved']  ) * 5)
      yellow = ((p['yellow_cards_y']  ))
      minutes = p['minutes'] / 30
      pts = xga + cs + gc + pens + saves + yellow + minutes
      pl = {
        'name':p['full_name'],
        'team': p['Team'],
        'pos':p['pos_y'],
        'pts':pts,
        'cost':p['now_cost']
      }
      if(p['time'] > -1):
        gks.append(pl)
    return gks

def defScoring(players):
    pl = {}
    gks = []
    for p in players:
      xga = ((p['xG'] * 6) + ((p['xA']) * 3))
      cs = ((p['clean_sheets']) * 4)
      gc = ((p['goals_conceded']) * -0.5)
      yellow = ((p['yellow_cards_y'] *-1 ))
      minutes = p['minutes'] / 30
      pts = xga + cs + gc + yellow + minutes
      pl = {
        'name':p['full_name'],
        'team': p['Team'],
        'pos':p['pos_y'],
        'pts':pts,
        'cost':p['now_cost']
      }
      if(p['time'] > -1):
        gks.append(pl)
    return gks

def midScoring(players):
    pl = {}
    gks = []
    for p in players:
      xga = ((p['xG'] * 5) + ((p['xA']) * 3))
      cs = ((p['clean_sheets']) * 1)
      yellow = ((p['yellow_cards_y'] *-1 ))
      minutes = p['minutes'] / 30
      pts = xga + cs + yellow + minutes
      pl = {
        'name':p['full_name'],
        'team': p['Team'],
        'pos':p['pos_y'],
        'pts':pts,
        'cost':p['now_cost']
      }
      if(p['time'] > -1):
        gks.append(pl)
    return gks

def fwdScoring(players):
    pl = {}
    gks = []
    for p in players:
      xga = ((p['xG'] * 4) + ((p['xA']) * 3))
      yellow = ((p['yellow_cards_y'] *-1 ))
      minutes = p['minutes'] / 30
      pts = xga  + yellow + minutes
      pl = {
        'name':p['full_name'],
        'team': p['Team'],
        'pos':p['pos_y'],
        'pts':pts,
        'cost':p['now_cost']
      }
      if(p['time'] > -1):
        gks.append(pl)
    return gks

def pickTeam(g,d,m,f):
    gk1 = g[12] # Cheapest gk, plays for Aston Villa so needs to be replaced
    gk2 = random.choice(g)
    while(gk1 == gk2):
        gk2 = random.choice(g)
    
    d1 = d[13] # Ben Johnson lowest def
    d2 = d[58] # Jarrad Branthwaite, lowest def
    #d2 = random.choice(d)
    #while(d1 == d2):
    #    d2 = random.choice(d)

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
    if(isLegal(team)):
      return findBestFormation(team)
    else:
        return [0,0,0]
      
    

def isLegal(team):
    price = 0
    teams = []
    for player in team:
        price += player['cost']
        teams.append(player['team'])

    if(price > 1000):
        return False

    ctr = Counter(teams)
    
    for k,v in ctr.items():
        if (v > 3):
            return False
    

    return True

def calculatePoints(team):
    pts = 0
    for p in team:
      pts += p['pts']
    
    return pts
  

def findBestFormation(team):
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

#fill player positions
gks = fillPlayers(players,'GK')
defs = fillPlayers(players, 'D')
mids = fillPlayers(players,'M')
fwds = fillPlayers(players,'F')

gks = gkScoring(gks)
defs = defScoring(defs)
mids = midScoring(mids)
fwds = fwdScoring(fwds)

#Set this for number of attempts
attempts = 10000000
counter = 0

best_team = []
best_points = 0
best_formation = ''
start = time.time()
print("run simulation")
while(counter < attempts):
    if not(counter % 100000):
        print(counter / attempts)
        #print(best_points)
        #print('------------')
        #print(best_formation)
        #print('------------')
    counter += 1
    team = pickTeam(gks,defs,mids,fwds)
    if(team[1] > best_points):
        best_team = team[0]
        best_points = team[1]
        best_formation = team[2]
end = time.time()

print('Finished ' + str(attempts) + ' in ' + str((end - start)) + ' seconds') 
print('------------')
print(best_team)
print('------------')
print(best_points)
print('------------')
print(best_formation)
print('------------')





