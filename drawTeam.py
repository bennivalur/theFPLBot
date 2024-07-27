from PIL import Image, ImageDraw
from PIL import ImageFont


def isPlural(transfers):
    if len(transfers) > 2:
        return 's'
    else:
        return ''

def drawTeam(formation, players,file_name,transfers):

    print("formation: " + formation)
    
    g = sorted(list(filter(lambda d: d['pos'] == 'GK', players)),key=lambda k: k['pts'],reverse=True)
    d = sorted(list(filter(lambda d: d['pos'] == 'D', players)),key=lambda k: k['pts'],reverse=True)
    m = sorted(list(filter(lambda d: d['pos'] == 'M', players)),key=lambda k: k['pts'],reverse=True)
    f = sorted(list(filter(lambda d: d['pos'] == 'F', players)),key=lambda k: k['pts'],reverse=True)
    players=g+d+m+f

    for p in players:
        print(p)
    field_width = 680
    field_length = 1050

    corner_to_box = 138.4

    goal_width = 73.2
    box_length = 165
    gk_box = 55
    penalty_spot = 115
    radius = 91.5

    player_size = 95 
    gk_w = (field_width / 2) - player_size/2
    gk_h = 30

    #Y placement of position lines
    s_h = 450
    d_h = 190
    m_h = 350
    f_h = 520

    if(len(transfers) > 0):
        transfers_width = 400
    else:
        transfers_width = 0
    #Init picture
    im = Image.new('RGB', (field_width + transfers_width, field_length-100), (0, 128, 0))
    draw = ImageDraw.Draw(im)
    font = ImageFont.truetype("Roboto-Black.ttf", 20)

    #Midfield line
    draw.rectangle((0, 0, field_width, field_length/2), outline=(255, 255, 255),width=10)
    #Side and end lines
    draw.rectangle((0, 0, field_width, field_length), outline=(255, 255, 255),width=10)
    #16yard box
    draw.rectangle((corner_to_box, 0,  corner_to_box + (box_length*2) + goal_width, 165), outline=(255, 255, 255),width=10)
    #6yard box
    draw.rectangle((corner_to_box + (box_length-gk_box), 0,  corner_to_box + (box_length) + goal_width + gk_box, gk_box), outline=(255, 255, 255),width=10)

    #Penalty Spot
    draw.ellipse((field_width/2, penalty_spot, (field_width/2)+10, penalty_spot+10),outline=(255, 255, 255),width=10)
    
    #D-bow
    draw.arc(((field_width/2)-radius, penalty_spot-radius, (field_width/2)+radius, penalty_spot+radius), 30, 150, 'white',width=10) 
    #Midfield circle
    draw.ellipse(((field_width/2)-radius, (field_length/2)-radius, (field_width/2)+radius,(field_length/2)+radius), outline=(255, 255, 255),width=10)

    #Corner Rings
    draw.arc((-30, -30, 50,50),  0, 360, 'white',width=10)
    draw.arc((field_width-50, -30, field_width+30,50),  0, 360, 'white',width=10)

    #Midfiled marker
    draw.rectangle(((field_width/2)-5, (field_length/2)-20,(field_width/2)+5, (field_length/2)+10), outline=(255, 255, 255),width=10)

    #Bench box
    draw.rectangle((0, field_length-300, field_width, field_length-100), fill=(46, 162, 219), outline=(5, 47, 82),width=10)

    
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
        w = field_width / (1+no_defenders)
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
        w = field_width / (1+no_midfielders)
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
        w = field_width / (1+no_forwards)

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
            b2 = players[10]
            b3 = players[11]
        elif(no_midfielders == 4):
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
    draw.rectangle((0, field_length-400, field_width, field_length-300), fill=(46, 162, 219), outline=(5, 47, 82),width=10)
    txt = 'Expected Points: ' + str(round(pts,2)) + ' | Cost: ' + str(round(cost,2))
    draw.text((field_width/2,field_length-340),txt,(0,0,0),anchor='ms',font=font)

    #Draw Tranfer section if transfers were made
    if(len(transfers) > 0):
        font = ImageFont.truetype("Roboto-Black.ttf", 15)
        draw.rectangle((field_width,0, field_width+transfers_width, field_length-100), fill=(46, 162, 219), outline=(5, 47, 82),width=10)
        if transfers[0] != 'none':
            
            draw.polygon([(field_width+250,field_length/2 - 200), (field_width+300, field_length/2-175), (field_width+250,field_length/2-150)], fill = (0,0,0))
            draw.polygon([(field_width+175,field_length/2 - 145), (field_width+125, field_length/2-120), (field_width+175,field_length/2-95)], fill = (0,0,0))

            draw.rectangle((field_width+175,field_length/2-185, field_width+250, field_length/2-165), fill='black')
            draw.rectangle((field_width+175,field_length/2-130, field_width+250, field_length/2-110), fill='black')

            draw.arc((field_width+225,field_length/2-150, field_width+265,field_length/2-110),  -30, 90, 'black',width=30)
            draw.arc((field_width+155,field_length/2-185, field_width+195,field_length/2-145),  120, -90, 'black',width=30)
            
            for index, t in enumerate(transfers):
                
                if index < len(transfers)/2:
                    w = (transfers_width / (1+(len(transfers)/2)))
                    #text_buffer = 100
                    slider = 0
                    if(len(transfers) > 6):
                        w = transfers_width / 4
                        if(index < 3):
                            d_h = 70
                            slider = 0
                        else:
                            d_h = 200
                            slider = 3
                            
                    
                    draw.rectangle((field_width + w + (w*(index-slider))-player_size/2, d_h, field_width + w + (w*(index-slider))+player_size/2 , d_h + player_size), fill=t['color'])
                    draw.text((field_width + w+(w*(index-slider)) ,d_h+player_size+20),t['short'],(0,0,0),anchor='ms',font=font)
                    #Black stripes and cost and price
                    draw.rectangle((field_width + w+(w*(index-slider))-player_size/2, d_h+player_size-20, field_width +w+(w*(index-slider)) + player_size/2, d_h + player_size), fill='black')
                    draw.rectangle((field_width +w+(w*(index-slider))-player_size/2, d_h, field_width +w+(w*(index-slider)) + player_size/2, d_h + 20), fill='black')
                    draw.text((field_width +w+(w*(index-slider)),d_h+18),str(t['pts']),(255,255,255),anchor='ms',font=font)
                    draw.text((field_width +w+(w*(index-slider)),d_h + player_size-2),str(t['cost']/10),(255,255,255),anchor='ms',font=font)
                else:
                    
                    w =  (transfers_width / (1+(len(transfers)/2)))
                    s_index = index - (len(transfers)/2)

                    if(len(transfers) > 6):
                        #s_index -= 3
                        w = transfers_width / 4
                        if(index < (3 + len(transfers)/2)):
                            s_h = 440
                            slider = 0
                        else:
                            s_h = 570
                            slider = 3
    
                    
                    draw.rectangle((field_width +w + (w*(s_index-slider))-player_size/2, s_h, field_width +w + (w*(s_index-slider))+player_size/2 , s_h + player_size), fill=t['color'])
                    draw.text((field_width +w+(w*(s_index-slider)) ,s_h+player_size+20),t['short'],(0,0,0),anchor='ms',font=font)
                    
                    #Black stripes and cost and price
                    draw.rectangle((field_width +w+(w*(s_index-slider))-player_size/2, s_h+player_size-20, field_width +w+(w*(s_index-slider)) + player_size/2, s_h + player_size), fill='black')
                    draw.rectangle((field_width +w+(w*(s_index-slider))-player_size/2, s_h, field_width +w+(w*(s_index-slider)) + player_size/2, s_h + 20), fill='black')
                    draw.text((field_width +w+(w*(s_index-slider)),s_h+18),str(t['pts']),(255,255,255),anchor='ms',font=font)
                    draw.text((field_width +w+(w*(s_index-slider)),s_h + player_size-2),str(t['cost']/10),(255,255,255),anchor='ms',font=font)
            
            text_buffer = 0
            if(len(transfers) > 6):
                text_buffer = player_size + 10
            draw.text((field_width + transfers_width/2,gk_h+130 -text_buffer),'Transfer' + isPlural(transfers) + ' In',(0,0,0),anchor='ms',font=ImageFont.truetype("Roboto-Black.ttf", 30))
            draw.text((field_width + transfers_width/2,s_h+160 ),'Transfer' + isPlural(transfers) + ' Out',(0,0,0),anchor='ms',font=ImageFont.truetype("Roboto-Black.ttf", 30))

        else:
            draw.text((field_width + transfers_width/2,gk_h+130),'Amazing!' ,(0,0,0),anchor='ms',font=ImageFont.truetype("Roboto-Black.ttf", 30))
            draw.text((field_width + transfers_width/2,gk_h+160),'I was not able to find any transfers' ,(0,0,0),anchor='ms',font=ImageFont.truetype("Roboto-Black.ttf", 20))
            draw.text((field_width + transfers_width/2,gk_h+190),'to help make your team better' ,(0,0,0),anchor='ms',font=ImageFont.truetype("Roboto-Black.ttf", 20))

        img = Image.open('profilepic.PNG', 'r')
        img_w, img_h = img.size
        img_slider = 190
        if(len(transfers) > 6):
            img_w = int(img_w/1.5)
            img_h = int(img_h/1.5)
            img = img.resize((img_w,img_h))
            img_slider = 170
        offset = ((field_width+(transfers_width - img_w)//2) , (field_length - img_h-img_slider))
        im.paste(img, offset)
        font = ImageFont.truetype("Roboto-Black.ttf", 20)
        draw.text(((field_width+(transfers_width/2)) , (field_length - 155)),'Made by @bennivaluR_ for @theFPLBot',(0,0,0),anchor='ms',font=font)
        draw.text(((field_width+(transfers_width/2)) , (field_length - 130) ),'www.thefplbot.com',(0,0,0),anchor='ms',font=font)


    im.save('transfers/' + file_name + '.png', quality=95)

