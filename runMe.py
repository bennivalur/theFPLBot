import json
from dataGet import *
from dataMerge import *
from projectSeason import *
from buildSquad import buildSquad, buildSmartSquad
from suggestTransfer import suggestTransfers,getTeam,convertFPLteam
from drawTeam import drawTeam
from drawRankings import drawRankings
#Flags
isPreseason = True
getHistory = False
getNewData = False
buildRandom = False
buildSmart = True


#Get data
if getNewData:
    getFPLPlayerAndMatchData()
    getUnderstatPlayers()

    #Check what players are missing from merge files
    #Check what FPL players don't have a match
    findMissingFPLPlayers()
    #Check what understat players don't have a match
    findMissingUnderstatPlayers()

    #Merge data
    mergeDataSets()
if getHistory:
    getHistoricUnderstatData()
    getFPLPlayerHistory()
    getUnderstatPlayerHistory()

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


#Make Weekly projections

    #Calculate Clean sheet chances

    #Update players Goals Over Expected (finishing rating)

#Print team

#Keep Track of league

#Keep track of individual performance relative to everyone else
