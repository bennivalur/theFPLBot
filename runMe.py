from getData import getData, findMissingPlayers
from projections import makeProjections
from getLeagueResults import getSeasons
from predictCS import predictCS, getNextGameWeek
from fpl import buildSquad
from suggestTransfer import suggestTransfers,getTeam,convertFPLteam
from drawTeam import drawTeam
from drawRankings import drawRankings
import requests


form_range = 5


week = getNextGameWeek()
print("Getting data for week: " + str(week))
getData(week)
findMissingPlayers()
predictCS()
makeProjections()

team = getTeam(249795,week-1)
capital = team['entry_history']['value'] + team['entry_history']['bank']
squad = convertFPLteam(team['picks'])

#Only for preseason or wildcard
#squad = buildSquad(10)

suggested = suggestTransfers(squad,1,capital)
drawTeam(suggested[0],suggested[1],'week_' + str(week) + '_transfers',suggested[2])

