from getData import getData
from projections import makeProjections
from getLeagueResults import getSeasons
from predictCS import predictCS, getNextGameWeek
import requests


form_range = 5

#print("Getting data for week: " + str(week))
week = getNextGameWeek() - 1
getData(week)
predictCS()
makeProjections()