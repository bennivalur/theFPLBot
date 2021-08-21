from PIL import Image, ImageDraw
from PIL import ImageFont

def drawRankings(pos,week):
    width = 1000
    height = 1000

    im = Image.new('RGB', (width, height), (0, 128, 0))
    draw = ImageDraw.Draw(im)
    font = ImageFont.truetype("Roboto-Black.ttf", 20)


    im.save('positionsProjections/week_' + str(week) + '_' + pos + '_projections' + '.png', quality=95)
    print('aha')