from getData import getData, findMissingPlayers,getFPL,getLeague,getNextGameWeek
from projections import makeProjections
from getLeagueResults import getSeasons
from predictCS import predictCS
from checkOdds import checkBets, checkBetResults
from fpl import buildSquad, buildSmartSquad
from suggestTransfer import suggestTransfers,getTeam,convertFPLteam
from drawTeam import drawTeam
from drawRankings import drawRankings
from drawLeague import drawLeague
import pandas as pd

#How many games back we look at
form_range = 5

week = getNextGameWeek()
if_getData = True
teamToGet = 576373

if_suggestTransfers = True
if_makeTeamFromScratch = False
if_drawRankings = True
if_drawBotsLeague = True
if_checkBets = True

if if_getData:
    print("Getting data for week: " + str(week))
    getData(week)

    #Logs players who have played in the PL this season but do not yet hava an ID match in our match file
    findMissingPlayers()

    #Predict clean sheet odds
    predictCS()

    makeProjections()

if teamToGet != -1 and if_suggestTransfers:
    #Get players on the team of the bot
    team = getTeam(teamToGet,week-1)
    #team = getTeam(31003,week-1)
    squad = convertFPLteam(team['picks'])

    capital = team['entry_history']['value'] ##+ team['entry_history']['bank']
    print("capital:" + str(capital))
    suggested = suggestTransfers(squad,1,capital)
    drawTeam(suggested[0],suggested[1],'week_' + str(week) + '_transfers',suggested[2])
    
#Only for preseason or wildcard - builds a squad from scratch
if if_makeTeamFromScratch:
    
    squad = buildSquad(1000)
    capital = 100
    squad = buildSmartSquad(1000)
    drawTeam(suggested[0],suggested[1],'preseason23_24',suggested[2])

if if_drawRankings:
    #Draw position rankings
    drawRankings('GK',week,10)
    drawRankings('D',week,15)
    drawRankings('M',week,15)
    drawRankings('F',week,15)

#Get latest standings for the BotsVsBots league
if if_drawBotsLeague:
    getLeague(106519)
    drawLeague(week)

#compare my models odds of keeping a clean sheet to the odds of lengjan.is
if if_checkBets:
    checkBets()
    #Input = betting_amount,bet_margin
    checkBetResults(10000,0.00)