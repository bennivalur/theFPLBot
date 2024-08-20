import copy
import json,urllib
import itertools

def trackPerformance(teamToGet,week):

    with open('data/performanceTracking/overallTrack.json','r') as overalltrack:
        overalltrack = json.load(overalltrack)

    if overalltrack[-1]['entry_history']['event'] < week-1:
        try:
            print("Getting Event Entry")
            with urllib.request.urlopen("https://fantasy.premierleague.com/api/entry/"+ str(teamToGet) +"/event/"+ str(week) +"/picks/") as url:
                data = json.loads(url.read().decode())
                
                overalltrack = overalltrack.append(data)
                with open('data/performanceTracking/overallTrack.json', 'w') as file:
                    file.write(json.dumps(overalltrack))      
        except:
            return 'error'
    else:
        print("Latest Track already on file")
    #TODO make a trend graphic or something