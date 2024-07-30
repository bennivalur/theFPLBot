from datetime import datetime

def getCurrentSeasonStartYear():
    year = datetime.now().year
    month = datetime.now().month
    if(month < 7):
        return str(year-1)
    else:
        return str(year)