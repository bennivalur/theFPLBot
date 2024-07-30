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
    getFPLPlayerHistory()
    getUnderstatPlayerHistory()

if isPreseason:
    #make full season projection
    makeSeasonProjections()
    #pick preseason team
    projectionSource = '2024_2025_preseason'
    capital = 100
    squad = buildSquad(100000,projectionSource)
    #suggested = suggestTransfers(squad,1,capital,projectionSource)
    #drawTeam(suggested[0],suggested[1],'preseason24_25_random',suggested[2])
    squad = buildSmartSquad(100000,projectionSource)
    #suggested = suggestTransfers(squad,1,capital,projectionSource)
    #drawTeam(suggested[0],suggested[1],'preseason24_25_smart',suggested[2])


#Make Weekly projections

    #Calculate Clean sheet chances

    #Update players Goals Over Expected (finishing rating)

#Print team

#Keep Track of league

#Keep track of individual performance relative to everyone else
