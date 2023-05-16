from getData import getData, findMissingPlayers,getFPL,getLeague
from projections import makeProjections
from getLeagueResults import getSeasons
from predictCS import predictCS, getNextGameWeek, checkBets, checkBetResults
from fpl import buildSquad
from suggestTransfer import suggestTransfers,getTeam,convertFPLteam
from drawTeam import drawTeam
from drawRankings import drawRankings
from drawLeague import drawLeague
import pandas as pd

#How many games back we look at
form_range = 5

getFPL()
week = getNextGameWeek()
print("Getting data for week: " + str(week))
getData(week)

#Logs players who have played in the PL this season but do not yet hava an ID match in our match file
findMissingPlayers()

#Predict clean sheet odds
predictCS()

#makeProjections()

#Get players on the team of the bot
team = getTeam(3939796,week-1)
squad = convertFPLteam(team['picks'])

capital = team['entry_history']['value'] ##+ team['entry_history']['bank']
print("capital:" + str(capital))

#Only for preseason or wildcard - builds a squad from scratch
#squad = buildSquad(100000000)


suggested = suggestTransfers(squad,10,capital)
drawTeam(suggested[0],suggested[1],'week_' + str(week) + '_transfers',suggested[2])
#drawTeam(suggested[0],suggested[1],'preseason22_23',suggested[2])

#Draw position rankings
drawRankings('GK',week,10)
drawRankings('D',week,15)
drawRankings('M',week,15)
drawRankings('F',week,15)

#Get latest standings for the BotsVsBots league
getLeague(850313)
drawLeague(week)

#compare my models odds of keeping a clean sheet to the odds of lengjan.is

checkBets()
#Input = betting_amount,bet_margin
#checkBetResults(10000,0.00)