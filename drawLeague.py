from PIL import Image, ImageDraw
from PIL import ImageFont
import json

width = 850
height = 1050


header = 100
table_header_height = 50

columns = [150,550,700,850]
column_names = ['Pos','Team','GW PTS','Total PTS']

#Draw separator lines between columns
def drawLines(draw,numberOf,img_h):
    player_height = (height - header - table_header_height - img_h) / (numberOf)
    font = ImageFont.truetype("Roboto-Black.ttf", 20)

    draw.rectangle((0,0, width,header + height+table_header_height), fill=(46, 162, 219), outline=(5, 47, 82),width=10)
    draw.rectangle((0,header, width,header+10), fill=(5, 47, 82), outline=(5, 47, 82),width=0)
    draw.rectangle((0,header + table_header_height, width,header+ table_header_height+10), fill=(5, 47, 82), outline=(5, 47, 82),width=0)

    for index, column in enumerate(columns):
        draw.rectangle((column,header, column+10,header + table_header_height + (player_height*numberOf)), fill=(5, 47, 82), outline=(5, 47, 82))

        if(index > 0):
            draw.text(((columns[index] - columns[index-1])/2 + columns[index-1],header+table_header_height/2+20),column_names[index],(0, 0, 0),anchor='ms',font=font)
        else:
            draw.text(((columns[index])/2 ,header+table_header_height/2+20),column_names[index],(0, 0, 0),anchor='ms',font=font)

#fill the table with the data about the participants and standing
def fillPlayers(draw,players,img_h):
    player_height = (height - header - table_header_height - img_h) / len(players)
    
    font = ImageFont.truetype("Roboto-Light.ttf", 25)
    smallfont = ImageFont.truetype("Roboto-Light.ttf", 22)
    for index, p in enumerate(players):
       
        draw.rectangle((0,header + table_header_height+((index+1)*player_height), width,header + table_header_height+((index+1)*player_height)+10), fill=(5, 47, 82), outline=(5, 47, 82),width=0)
        
        texts = ['',p['entry_name'],str(p['event_total']),str(p['total'])]

        for index2, text in enumerate(texts):
            if(index2 > 0):
                draw.text((((columns[index2]-columns[index2-1])/2)+columns[index2-1],header+table_header_height+((1+index)*player_height)-(player_height/2)+20),text,(0, 0, 0),anchor='ms',font=smallfont)
            else:
                draw.text((((columns[index2])/2)-40,header+table_header_height+((1+index)*player_height)-(player_height/2)+20),str(p['rank']),(0, 0, 0),anchor='ms',font=smallfont)
                if(p['last_rank'] < p['rank']):
                    draw.polygon([((columns[0]/2)-20,-5+header+table_header_height+((1+index)*player_height)-(player_height/2)), ((columns[0]/2), -5+header+table_header_height+((1+index)*player_height)-(player_height/2)+25), ((columns[0]/2)+20,-5+header+table_header_height+((1+index)*player_height)-(player_height/2))], fill = (255,0,0))
                    draw.text((((columns[index2])/2)+40,header+table_header_height+((1+index)*player_height)-(player_height/2)+20),'('+str(p['last_rank'] - p['rank'])+')',(0, 0, 0),anchor='ms',font=smallfont)
                elif(p['last_rank'] > p['rank']):
                    draw.polygon([((columns[0]/2)-20,-5+header+table_header_height+((1+index)*player_height)-(player_height/2)+25), ((columns[0]/2), -5+header+table_header_height+((1+index)*player_height)-(player_height/2)), ((columns[0]/2)+20,-5+header+table_header_height+((1+index)*player_height)-(player_height/2)+25)], fill = (0,255,0))
                    draw.text((((columns[index2])/2)+40,header+table_header_height+((1+index)*player_height)-(player_height/2)+20),'(+'+str(p['last_rank'] - p['rank'])+')',(0, 0, 0),anchor='ms',font=smallfont)

def drawLeague(week):
    with open('tempfiles/botsvsbots.json','r') as main_pl:
        entries = json.load(main_pl)
    
    players = entries[-1]['standings']['results']
    """
    for p in players:
        print(p)"""

    im = Image.new('RGB', (width, header + height+table_header_height), (0, 0, 0))
    draw = ImageDraw.Draw(im)
    
    img = Image.open('profilepic.PNG', 'r')
    img_w, img_h = img.size

    numberOf = len(players)
    drawLines(draw,numberOf,img_h)

    fillPlayers(draw,players,img_h)

    #Draw Header
    font = ImageFont.truetype("Roboto-Black.ttf", 45)
    draw.text((width/2,header/2+30),'Bots vs. Bots League Standings: Week ' + str(week-1),(0, 0, 0),anchor='ms',font=font)

    #Draw image and credits
    offset = ((50,(height - ((height - header - table_header_height - img_h))/2)+img_h *1.25))
   
    offset = (int(offset[0]),int(offset[1]))
    im.paste(img, offset)
    font = ImageFont.truetype("Roboto-Black.ttf", 30)
    draw.text((50+width*0.5,((height - ((height - header - table_header_height - img_h))/2)+img_h *1.8)),'Made by @bennivaluR_ for @theFPLBot',(0,0,0),anchor='ms',font=font)
    draw.text((50+width*0.5,((height - ((height - header - table_header_height - img_h))/2)+img_h *2)),'www.thefplbot.com',(0,0,0),anchor='ms',font=font)


    im.save('botsvsbots/week_' + str(week-1) + '_standings.png', quality=95)