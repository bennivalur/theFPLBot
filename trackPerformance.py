import copy
import json,urllib
import itertools

def trackPerformance(teamToGet,week):

    with open('data/performanceTracking/overallTrack.json','r') as overalltrack:
        overalltrack = json.load(overalltrack)

    if overalltrack[-1]['event'] < week-1:
        
            print("Getting Event Entry")
            urllink = "https://fantasy.premierleague.com/api/entry/"+ str(teamToGet) +"/event/"+ str(week-1) +"/picks/"
            
            with urllib.request.urlopen(urllink) as url:
                data = json.loads(url.read().decode())
                
                overalltrack.append(data['entry_history'])

                with open('data/performanceTracking/overallTrack.json', 'w') as file:
                    file.write(json.dumps(overalltrack))      
        
    else:
        print("Latest Track already on file")
    #TODO make a trend graphic or something