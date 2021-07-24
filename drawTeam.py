from PIL import Image, ImageDraw
from PIL import ImageFont

def drawTeam(formation, players):
    field_with = 680
    field_length = 1050

    corner_to_box = 138.4

    goal_width = 73.2
    box_length = 165
    gk_box = 55
    penalty_spot = 115
    radius = 91.5

    player_size = 100 
    gk_w = (field_with / 2) - player_size/2
    gk_h = 30

    #Y placement of position lines
    d_h = 190
    m_h = 350
    f_h = 520

    #Init picture
    im = Image.new('RGB', (field_with, field_length-100), (0, 128, 0))
    draw = ImageDraw.Draw(im)
    font = ImageFont.truetype("Roboto-Black.ttf", 20)
    
    #Midfield
    draw.rectangle((0, 0, field_with, field_length/2), outline=(255, 255, 255),width=10)
    #Side and end lines
    draw.rectangle((0, 0, field_with, field_length), outline=(255, 255, 255),width=10)
    #16yard box
    draw.rectangle((corner_to_box, 0,  corner_to_box + (box_length*2) + goal_width, 165), outline=(255, 255, 255),width=10)
    #6yard box
    draw.rectangle((corner_to_box + (box_length-gk_box), 0,  corner_to_box + (box_length) + goal_width + gk_box, gk_box), outline=(255, 255, 255),width=10)

    #Penalty Spot
    draw.ellipse((field_with/2, penalty_spot, (field_with/2)+10, penalty_spot+10),outline=(255, 255, 255),width=10)
    
    #D-bow
    draw.arc(((field_with/2)-radius, penalty_spot-radius, (field_with/2)+radius, penalty_spot+radius), 30, 150, 'white',width=10) 
    #Midfield circle
    draw.ellipse(((field_with/2)-radius, (field_length/2)-radius, (field_with/2)+radius,(field_length/2)+radius), outline=(255, 255, 255),width=10)

    #Corner Rings
    draw.arc((-30, -30, 50,50),  0, 360, 'white',width=10)
    draw.arc((field_with-50, -30, field_with+30,50),  0, 360, 'white',width=10)

    #Midfiled marker
    draw.rectangle(((field_with/2)-5, (field_length/2)-20,(field_with/2)+5, (field_length/2)+10), outline=(255, 255, 255),width=10)

    #Bench box
    draw.rectangle((0, field_length-300, field_with, field_length-100), fill=(46, 162, 219), outline=(5, 47, 82),width=15)

    #Sort goalkeepers
    gks = list(filter(lambda d: d['pos'] == 'GK', players))
    if(gks[0]['pts'] > gks[1]['pts']):
        gk1 = gks[0]
        gk2 = gks[1]
    else:
        gk1 = gks[1]
        gk2 = gks[0]

    #GK box
    draw.rectangle((gk_w, gk_h, gk_w + player_size, gk_h + player_size), fill=gk1['color'])
    #Gk name
    draw.text((gk_w+player_size/2,gk_h+player_size+20),gk1['short'],(0,0,0),anchor='ms',font=font)
    
    #Black stripes
    draw.rectangle((gk_w, gk_h+player_size-20, gk_w + player_size, gk_h + player_size), fill='black')
    draw.rectangle((gk_w, gk_h, gk_w + player_size, gk_h + 20), fill='black')
    #Cost and points
    draw.text((gk_w+player_size/2,gk_h+18),str(gk1['pts']),(255,255,255),anchor='ms',font=font)
    draw.text((gk_w+player_size/2,gk_h + player_size-2),str(gk1['cost']/10),(255,255,255),anchor='ms',font=font)

    no_defenders = int(formation[0])
    for x in range(0,no_defenders):
        p = players[2+x]
        w = field_with / (1+no_defenders)

        #box and name
        draw.rectangle((w + (w*x)-player_size/2, d_h, w + (w*x)+player_size/2 , d_h + player_size), fill=p['color'])
        draw.text((w+(w*x) ,d_h+player_size+20),p['short'],(0,0,0),anchor='ms',font=font)

        #Black stripes and cost and price
        draw.rectangle((w+(w*x)-player_size/2, d_h+player_size-20, w+(w*x) + player_size/2, d_h + player_size), fill='black')
        draw.rectangle((w+(w*x)-player_size/2, d_h, w+(w*x) + player_size/2, d_h + 20), fill='black')
        draw.text((w+(w*x),d_h+18),str(p['pts']),(255,255,255),anchor='ms',font=font)
        draw.text((w+(w*x),d_h + player_size-2),str(p['cost']/10),(255,255,255),anchor='ms',font=font)
    
    no_midfielders = int(formation[2])
    for x in range(0,no_midfielders):
        p = players[7+x]
        w = field_with / (1+no_midfielders)

        #box and name
        draw.rectangle((w + (w*x)-player_size/2, m_h, w + (w*x)+player_size/2 , m_h + player_size), fill=p['color'])
        draw.text((w+(w*x) ,m_h+player_size+20),p['short'],(0,0,0),anchor='ms',font=font)

        #Black stripes and cost and price
        draw.rectangle((w+(w*x)-player_size/2, m_h+player_size-20, w+(w*x) + player_size/2, m_h + player_size), fill='black')
        draw.rectangle((w+(w*x)-player_size/2, m_h, w+(w*x) + player_size/2, m_h + 20), fill='black')
        draw.text((w+(w*x),m_h+18),str(p['pts']),(255,255,255),anchor='ms',font=font)
        draw.text((w+(w*x),m_h + player_size-2),str(p['cost']/10),(255,255,255),anchor='ms',font=font)

    no_forwards = int(formation[4])
    for x in range(0,no_forwards):
        p = players[12+x]
        w = field_with / (1+no_forwards)

        #box and name
        draw.rectangle((w + (w*x)-player_size/2, f_h, w + (w*x)+player_size/2 , f_h + player_size), fill=p['color'])
        draw.text((w+(w*x) ,f_h+player_size+20),p['short'],(0,0,0),anchor='ms',font=font)

        #Black stripes and cost and price
        draw.rectangle((w+(w*x)-player_size/2, f_h+player_size-20, w+(w*x) + player_size/2, f_h + player_size), fill='black')
        draw.rectangle((w+(w*x)-player_size/2, f_h, w+(w*x) + player_size/2, f_h + 20), fill='black')
        draw.text((w+(w*x),f_h+18),str(p['pts']),(255,255,255),anchor='ms',font=font)
        draw.text((w+(w*x),f_h + player_size-2),str(p['cost']/10),(255,255,255),anchor='ms',font=font)
    
    #Figure out which players are bench players depending on given formation
    if(no_defenders == 3):
        b1 = players[5]
        b2 = players[6]
        if(no_midfielders == 4):
            b3 = players[11]
        else:
            b3 = players[14]
    
    elif(no_defenders == 4):
        b1 = players[6]
        if(no_midfielders == 3):
            b2 = players[8]
            b3 = players[9]
        if(no_midfielders == 4):
            b2 = players[11]
            b3 = players[14]
        else:
            b2 = players[13]
            b3 = players[14]
    elif(no_defenders == 5):
        if(no_midfielders == 3):
            b1 = players[8]
            b2 = players[9]
            b3 = players[14]
        if(no_midfielders == 4):
            b1 = players[11]
            b2 = players[13]
            b3 = players[14]
        
    

    #BenchPlayers
    draw.rectangle((75, 800, 75 + player_size, 800 + player_size), fill=gk2['color'])
    draw.text((75+player_size/2, 800+player_size+20),gk2['short'],(0,0,0),anchor='ms',font=font)
    draw.rectangle((225, 800, 225 + player_size, 800 + player_size), fill=b1['color'])
    draw.text((225+player_size/2, 800+player_size+20),b1['short'],(0,0,0),anchor='ms',font=font)
    draw.rectangle((375, 800, 375 + player_size, 800 + player_size), fill=b2['color'])
    draw.text((375+player_size/2, 800+player_size+20),b2['short'],(0,0,0),anchor='ms',font=font)
    draw.rectangle((525, 800, 525 + player_size, 800 + player_size), fill=b3['color'])
    draw.text((525+player_size/2, 800+player_size+20),b3['short'],(0,0,0),anchor='ms',font=font)

    draw.rectangle((75, 800, 75 + player_size, 800 + 20), fill='black')
    draw.rectangle((75, 800+player_size-20, 75 + player_size, 800 + player_size), fill='black')
    draw.text((75+player_size/2,800+18),str(gk2['pts']),(255,255,255),anchor='ms',font=font)
    draw.text((75+player_size/2,800+player_size-2),str(gk2['cost']/10),(255,255,255),anchor='ms',font=font)

    draw.rectangle((225, 800, 225 + player_size, 800 + 20), fill='black')
    draw.rectangle((225, 800+player_size-20, 225 + player_size, 800 + player_size), fill='black')
    draw.text((225+player_size/2,800+18),str(b1['pts']),(255,255,255),anchor='ms',font=font)
    draw.text((225+player_size/2,800+player_size-2),str(b1['cost']/10),(255,255,255),anchor='ms',font=font)

    draw.rectangle((375, 800, 375 + player_size, 800 + 20), fill='black')
    draw.rectangle((375, 800+player_size-20, 375 + player_size, 800 + player_size), fill='black')
    draw.text((375+player_size/2,800+18),str(b2['pts']),(255,255,255),anchor='ms',font=font)
    draw.text((375+player_size/2,800+player_size-2),str(b2['cost']/10),(255,255,255),anchor='ms',font=font)

    draw.rectangle((525, 800, 525 + player_size, 800 + 20), fill='black')
    draw.rectangle((525, 800+player_size-20, 525 + player_size, 800 + player_size), fill='black')
    draw.text((525+player_size/2,800+18),str(b3['pts']),(255,255,255),anchor='ms',font=font)
    draw.text((525+player_size/2,800+player_size-2),str(b3['cost']/10),(255,255,255),anchor='ms',font=font)


    #calculate price & points
    pts = 0
    cost = 0
    for p in players:
        pts += p['pts']
        cost += p['cost']/10

    bench_pts = gk2['pts'] + b1['pts'] + b2['pts'] + b3['pts'] 
    pts = pts - bench_pts

    
    font = ImageFont.truetype("Roboto-Black.ttf", 30)

    #Points and cost
    draw.rectangle((0, field_length-400, field_with, field_length-300), fill=(46, 162, 219), outline=(5, 47, 82),width=15)
    txt = 'Points: ' + str(round(pts,2)) + ' | Cost: ' + str(cost)
    draw.text((field_with/2,field_length-340),txt,(0,0,0),anchor='ms',font=font)

    im.save('image.png', quality=95)

