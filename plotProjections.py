import json
import numpy as np
import time
from predictCS import getNextGameWeek

import matplotlib.pyplot as plt
from matplotlib.offsetbox import OffsetImage, AnnotationBbox

positions = [
    '0',
    'GK',
    'D',
    'M',
    'F',
]

positions_long = {
    'GK':'Goalkeepers',
    'D':'Defenderers',
    'M':'Midfielders',
    'F':'Forwards'
}

"""
        'projectionGraphs/'+ name + '_' + str(id) +'.png'
        # Upload image
        media = api.media_upload("profilepic.PNG")

        # Post tweet with image
        tweet = "..."
        post_result = api.update_status(status=tweet, media_ids=[media.media_id])
        

        api.update_status("I have changed my @ ")"""

def plotProjections(name,id):
    print("plot")

    with open('playerHistory/'+ name + '_' + str(id) + '.json','r') as fpl:
        player = json.load(fpl)

    _title = 'FPL Historical Points & Projected Points: '
    
    plot_credits = 'Data: Understat & FPL | plot by: @bennivaluR_'
    _file_name = 'projectionGraphs/'+ name + '_' + str(id) +'.png'

    

    player = player['history_past']

    with open('tempfiles/projections.json','r') as fpl:
        all_players = json.load(fpl)

    projected_player = next(x for x in all_players if x['fpl_id'] == id)
    print(projected_player)

    if(len(player) > 0):
        x = []
        points = []
        index = 1
        for s in player:
            x.append(s['season_name'])
            points.append(s['total_points'])
            index += 1
        
        x.append('2022/2023')
        points.append(projected_player['pts'])
    


        fig, ax = plt.subplots(figsize=(10,10))
        
        
        plt.plot(x,points)
        plt.plot(x,points,'s',label = 'Points',color="#2ea2db")
        plt.plot(['2021/2022'],[projected_player['pts']],'s',color ='#e78200')
        ax.set_facecolor('#3D315B')
        fig.set_facecolor('#3D315B')
        
        #plt.legend(loc="upper left")

        ax = plt.gca()

        plt.figtext(.5,.92,_title,color='#ffffff',fontsize=15,ha='center')
        sub_title = name + ' | ' + str(projected_player['pts']) + ' Projected Points'
        plt.figtext(.5,.90,sub_title,color='#ffffff',fontsize=12,ha='center')
        
        plt.figtext(.57, .03, plot_credits, fontsize=12,color='#ffffff')
        plt.ylabel('Points', fontsize=15,color='#ffffff')
        plt.xlabel('Season', fontsize=15,color='#ffffff')

        ax.spines['bottom'].set_color('white')
        ax.spines['top'].set_color('white') 
        ax.spines['right'].set_color('white')
        ax.spines['left'].set_color('white')
        ax.tick_params(axis='x', colors='white')
        ax.tick_params(axis='y', colors='white')
        ax.yaxis.label.set_color('white')
        ax.xaxis.label.set_color('white')

        if(len(player) == 1):
            plt.ylim([0, 250])

        #Save the figure as a png
        plt.savefig( _file_name,facecolor=fig.get_facecolor())

def plotTop(number):
    with open('tempfiles/projections.json','r') as fpl:
        all_players = json.load(fpl)


    players_to_plot = []
    for p in positions:
        if p != '0':
            players_to_plot += list(filter(lambda d: d['pos'] == p, all_players))[0:number]

    for pl in players_to_plot:
        plotProjections(pl['short'],pl['fpl_id'])