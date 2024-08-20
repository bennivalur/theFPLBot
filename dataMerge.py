import json
import csv
import pandas as pd
from timeFunctions import *

def mergeDataSets():
    print("Merge Datasets")
    fpl = pd.read_json('data/playerData/fpl_players.json')
    unders = pd.read_json('data/playerData/understat_players.json')

    fpl.rename(columns={'id': 'fpl_id'}, inplace=True)
    unders.rename(columns={'id':'understat'},inplace=True)

    fpl.to_csv('data/playerData/fpl_players.csv',index=False)
    unders.to_csv('data/playerData/understat_players.csv',index=False)
    keys = pd.read_csv('dataMergingFiles/Master.csv', low_memory=False)

    main_table = pd.merge(fpl,keys, on='code',how='inner')

    main_table = pd.merge(main_table,unders, on='understat',how='inner')
    #main_table = pd.merge(main_table,pos, on='fpl_id',how='inner')

    #player_teams = pd.merge(keys,unders,on='understat_id', how='inner')
    #player_teams.to_csv('teamshelper.csv',index=False)

    main_table.rename(columns={'team_x':'team'},inplace=True)

    

    main_table.to_csv('dataMergingFiles/maindata.csv',index=False)
    main_table.to_json('dataMergingFiles/maindata.json',orient='records')


def findMissingFPLPlayers():
    mergeKeys = pd.read_csv('dataMergingFiles/master.csv', low_memory=False)
    mergeKeys = mergeKeys['code'].tolist()
    
    #rint(mergeKeys)

    with open('data/playerData/fpl_players.json','r') as fpl:
        all_players = json.load(fpl)

    missingPlayers = []
    for p in all_players:
        if p['code'] not in mergeKeys:
            missingPlayers.append({
                'web_name': p['web_name'],
                'fpl_code':p['code'],
                'fpl_id':p['id']
            })
    
    with open('dataMergingFiles/MissingFPLPlayers.json', 'w') as file:
        file.write(json.dumps(missingPlayers))

    keys = missingPlayers[0].keys()

    with open('dataMergingFiles/MissingFPLPlayers.csv', 'w', encoding='utf8', newline='') as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(missingPlayers)

def findMissingUnderstatPlayers():
    mergeKeys = pd.read_csv('dataMergingFiles/master.csv', low_memory=False)
    mergeKeys = mergeKeys['understat'].tolist()
    
    with open('data/playerData/understat_players.json','r') as fpl:
        all_players = json.load(fpl)
    
    missingPlayers = []
    for p in all_players:
        if int(p['id']) not in mergeKeys:
            missingPlayers.append({
                'player_name': p['player_name'],
                'understat_id':p['id'],
            })
    if len(missingPlayers) != 0:
        keys = missingPlayers[0].keys()

        with open('dataMergingFiles/MissingUnderstatPlayers.csv', 'w', encoding='utf8', newline='') as output_file:
            dict_writer = csv.DictWriter(output_file, keys)
            dict_writer.writeheader()
            dict_writer.writerows(missingPlayers)