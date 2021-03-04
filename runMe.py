from getData import getData
from projections import makeProjections
from getLeagueResults import getSeasons
from predictCS import predictCS
import requests

week = 26
form_range = 5

#print("Getting data for week: " + str(week))

predictCS()
getData(week)
makeProjections()