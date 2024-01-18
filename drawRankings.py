from PIL import Image, ImageDraw
from PIL import ImageFont
import json

teams_pl = [
    '0',
    'Arsenal',
    'Aston Villa',
    'Bournemouth',
    'Brentford',
    'Brighton',
    'Burnley',
    'Chelsea',
    'Crystal Palace',
    'Everton',
    'Fulham',
    'Liverpool',
    'Luton',
    'Man City',
    'Man Utd',
    'Newcastle',
    'Nott\'m Forest',
    'Sheffield Utd',
    'Spurs',
    'West Ham',
    'Wolves'
]
teams_u = [
    {'title':'0','uid':-1},
    {'title':'Arsenal','uid': '83'},
    {'title':'Aston Villa','uid':'71'},
    {'title':'Bournemouth','uid':'-1'},
    {'title':'Brentford','uid':'244'},
    {'title':'Brighton','uid':'220'},
    {'title':'Burnley','uid':'-1'},
    {'title':'Chelsea', 'uid':'80'},
    {'title':'Crystal Palace','uid':'78'},
    {'title':'Everton','uid':'72'},
    {'title':'Fulham','uid':'-1'},
    {'title':'Liverpool','uid':'87'},
    {'title':'Luton Town','uid':'-1'},
    {'title':'Manchester City','uid':'88'},
    {'title':'Manchester United','uid':'89'},
    {'title':'Newcastle United','uid':'86'},
    {'title':'Nottingham Forest','uid':'-1'},
    {'title':'Sheffield United','uid':'-1'},
    {'title':'Tottenham','uid':'82'},
    {'title':'West Ham', 'uid':'81'},
    {'title':'Wolverhampton Wanderers','uid':'229'},
]

teams = [
    {'team': '0', 'title': '0', 'uid': -1},
    {'team': 'Arsenal', 'title': 'Arsenal', 'uid': '83'},
    {'team': 'Aston Villa', 'title': 'Aston Villa', 'uid': '71'},
    {'team': 'Brentford', 'title': 'Brentford', 'uid': '244'},
    {'team': 'Brighton', 'title': 'Brighton', 'uid': '220'},
    {'team': 'Burnley', 'title':'Burnley','uid':'-1'},
    {'team': 'Bournemouth', 'title': 'Bournemouth', 'uid': '-1'},
    {'team': 'Chelsea', 'title': 'Chelsea', 'uid': '80'},
    {'team': 'Crystal Palace', 'title': 'Crystal Palace', 'uid': '78'},
    {'team': 'Everton', 'title': 'Everton', 'uid': '72'},
    {'team': 'Liverpool', 'title': 'Liverpool', 'uid': '87'},
    {'team': 'Luton','title':'Luton Town','uid':'-1'},
    {'team': 'Man City', 'title': 'Manchester City', 'uid': '88'},
    {'team': 'Man Utd', 'title': 'Manchester United', 'uid': '89'},
    {'team': 'Newcastle', 'title': 'Newcastle United', 'uid': '86'},
    {'team': 'Nott\'m Forest', 'title': 'Nottingham Forest', 'uid': '-1'},
    {'team': 'Sheffield Utd','title':'Sheffield United','uid':'-1'},
    {'team': 'Spurs', 'title': 'Tottenham', 'uid': '82'},
    {'team': 'Fulham', 'title': 'Fulham', 'uid': '-1'},
    {'team': 'West Ham', 'title': 'West Ham', 'uid': '81'},
    {'team': 'Wolves', 'title': 'Wolverhampton Wanderers', 'uid': '229'}
]

width = 850
height = 1050


header = 100
table_header_height = 50

columns = [50,250,550,650,750,850]
column_names = ['color','Name','Team vs Opponent','PTS','CS%','Price']

def getTeam(team):
    return list(filter(lambda d: d['title'] == team, teams))[0]['team']

def getTitle(team):
    if(team == "Nott'm Forest"):
        return teams[15]['title']
    return list(filter(lambda d: d['team'] == team, teams))[0]['title']

def getPosition(pos):
    short = ['GK','D','M','F']
    full = ['Goalkeeper','Defender', 'Midfielder','Forward']
    
    return full[short.index(pos)]

#Draw sepearot lines
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

#Populate fields with data
def fillPlayers(draw,pos,numberOf,img_h):
    player_height = (height - header - table_header_height - img_h) / (numberOf)
    with open('tempfiles/projections.json','r') as main_pl:
        all_players = json.load(main_pl)
    
    with open('tempfiles/clean_sheet_odds.json','r') as cs:
        clean_sheets = json.load(cs)

    #Filter by position
    players = list(filter(lambda d: d['pos'] == pos, all_players))[0:numberOf]

    
    

    font = ImageFont.truetype("Roboto-Light.ttf", 25)
    smallfont = ImageFont.truetype("Roboto-Light.ttf", 22)
    for index, p in enumerate(players):
       
        draw.rectangle((0,header + table_header_height+((index+1)*player_height), width,header + table_header_height+((index+1)*player_height)+10), fill=(5, 47, 82), outline=(5, 47, 82),width=0)
        draw.rectangle((10,10+header + table_header_height+((index)*player_height), columns[0],header + table_header_height+((index+1)*player_height)), fill=p['color'], outline=(5, 47, 82),width=0)

        teamTitle = getTitle(p['team'])
        cs = list(filter(lambda d: d['team'] == teamTitle, clean_sheets))[0]
        
        texts = ['',p['short'],p['team'] +' vs. ' + getTeam(cs['opponent']),str(p['pts']),str(round(cs['csOdds']*100,1))+'%',str(p['cost']/10)]

        if(pos == 'F' or pos == 'M'):
            del texts[4]   
        

        for index2, text in enumerate(texts):
            if(index2 > 0):
                draw.text((((columns[index2]-columns[index2-1])/2)+columns[index2-1],header+table_header_height+((1+index)*player_height)-(player_height/2)+20),text,(0, 0, 0),anchor='ms',font=smallfont)


def drawRankings(pos,week,numberOf):
    #Midfielders and forwards do not need the clean sheet column
    if(pos == 'F' or pos == 'M'):
        del columns[4]
        del column_names[4]

    im = Image.new('RGB', (width, header + height+table_header_height), (0, 0, 0))
    draw = ImageDraw.Draw(im)
    
    img = Image.open('profilepic.PNG', 'r')
    img_w, img_h = img.size

    drawLines(draw,numberOf,img_h)

    fillPlayers(draw,pos,numberOf,img_h)
    
    #Draw Header
    font = ImageFont.truetype("Roboto-Black.ttf", 45)
    draw.text((width/2,header/2+30),'Week ' + str(week) + ': Top ' + str(numberOf) + ' Projected ' + getPosition(pos) + 's',(0, 0, 0),anchor='ms',font=font)

    #Draw image and credits
    offset = ((50,(height - ((height - header - table_header_height - img_h))/2)+img_h *1.25))
   
    offset = (int(offset[0]),int(offset[1]))
    im.paste(img, offset)
    font = ImageFont.truetype("Roboto-Black.ttf", 30)
    draw.text((50+width*0.5,((height - ((height - header - table_header_height - img_h))/2)+img_h *1.8)),'Made by @bennivaluR_ for @theFPLBot',(0,0,0),anchor='ms',font=font)
    draw.text((50+width*0.5,((height - ((height - header - table_header_height - img_h))/2)+img_h *2)),'www.thefplbot.com',(0,0,0),anchor='ms',font=font)

    if(pos == 'F' or pos == 'M'):
        columns.insert(4,750)
        column_names.insert(4,'CS%')

    im.save('positionsProjections/week_' + str(week) + '_' + pos + '_projections' + '.png', quality=95)