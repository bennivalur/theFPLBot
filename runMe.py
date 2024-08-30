import json
from dataGet import *
from dataMerge import *
from projectSeason import *
from buildSquad import buildSquad, buildSmartSquad
from suggestTransfer import suggestTransfers,getTeam,convertFPLteam
from drawTeam import drawTeam
from projectWeek import makeWeeklyProjections
from trackPerformance import *
#Flags

getHistory = False
getNewData = False
isPreseason = False
buildRandom = False
buildSmart = False
teamToGet = 3904573
gameweek = getNextGameWeek()
season = 2024



if getHistory:
    getHistoricUnderstatData()
    getFPLPlayerHistory()
    getUnderstatPlayers(season-1)

#Get data
if getNewData:
    getFPLPlayerAndMatchData()
    getUnderstatPlayers(season)

    #Check what players are missing from merge files
    #Check what FPL players don't have a match
    findMissingFPLPlayers()
    #Check what understat players don't have a match
    findMissingUnderstatPlayers()

    #Merge data
    mergeDataSets()

if isPreseason:
    #make full season projection
    makeSeasonProjections()
    #pick preseason team
    projectionSource = '2024_2025_preseason'
    capital = 100
    
    if buildSmart:
        squad = buildSmartSquad(1000000,projectionSource)
    if buildRandom:
       squad = buildSquad(1000000000,projectionSource)

if not isPreseason:
    trackPerformance(teamToGet,gameweek)
    #TODO: Calculate Clean sheet chances
    makeWeeklyProjections(gameweek)
    
    team = getTeam(teamToGet,gameweek-1)
    squad = convertFPLteam(team['picks'],season,gameweek)

    capital = team['entry_history']['value'] ##+ team['entry_history']['bank']
    print("capital:" + str(capital))
    source = str(season) + '_' + str(season+1) + '/week_' + str(gameweek)
    suggested = suggestTransfers(squad,1,capital,source)
    drawTeam(suggested[0],suggested[1],'week_' + str(gameweek) + '_transfers',suggested[2])


#Print team

#Keep Track of league

#Keep track of individual performance relative to everyone else
