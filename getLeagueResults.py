import asyncio
import json
import os
import urllib.request
import aiohttp

from understat import Understat
async def main(league:str,season:str):
    async with aiohttp.ClientSession() as session:
        understat = Understat(session)
        results = await understat.get_league_results(
            league, season
        )

        print('Getting ' + league + ':' + season )
        results = json.dumps(results)
        with open('tempfiles/'+league+'_'+season+'_res.json', 'w') as file:
            file.write(results)

def getSeasons(league:str,season:str):
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(league,season))