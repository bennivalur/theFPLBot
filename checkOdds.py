import json
import urllib.request
from getData import fplFixtures
from teamsConfig import lengjan_teams

def checkBetResults(bet_amount,odds_margin):
    #fplFixtures(True)
    print("checking bet results")
    
    with open('tempfiles/bet_scheme.json', 'r') as all_bets:
        bets = json.load(all_bets)

    fplFixtures(True)

    with open('tempfiles/all_fpl_fixtures.json', 'r') as file:
        results = json.load(file)
    wins = 0
    losses = 0
    balance = 0
    for b in bets:
        if((float(b['myOdds']) - float(b['lengjanOdds'])) > odds_margin):
            g = next(item for item in results if item["code"] == b['fpl_code'])
            if(g['finished']):
                if(b['home_away'] == 'home'):
                    if(b['cS'] == 'Yes'):
                        if(g['team_a_score'] > 0):
                            balance -= bet_amount
                            losses += 1
                        else:
                            balance += bet_amount * (1/float(b['lengjanOdds']))
                            wins += 1
                    else:
                        if(g['team_a_score'] == 0):
                            balance += bet_amount * (1/float(b['lengjanOdds']))
                            wins += 1
                        else:
                            balance -= bet_amount
                            losses += 1
                else:
                    if(b['cS'] == 'Yes'):
                        if(g['team_h_score'] > 0):
                            balance -= bet_amount
                            losses += 1
                        else:
                            balance += bet_amount * (1/float(b['lengjanOdds']))
                            wins += 1
                    else:
                        if(g['team_h_score'] == 0):
                            balance += bet_amount * (1/float(b['lengjanOdds']))
                            wins += 1
                        else:
                            balance -= bet_amount
                            losses += 1

    print("wins: " + str(wins))
    print("losses: " + str(losses))            
    print("balance: " + str(balance))
    percentProf = balance /((wins + losses)*bet_amount + balance) * 100
    #percentProf = balance / starting_budget * 100
    print(str(round(percentProf,2)) + '%')

def checkBets():
    print("Checking Bets")
    with open('tempfiles/clean_sheet_odds.json', 'r') as all_games:
        games = json.load(all_games)


    #Get available bets from lengjan
    odds = urllib.request.urlopen("https://games.lotto.is/game/lengjan-events?live=0").read()
    odds = json.loads(odds)
    events = odds['events']

    #filter out games that are not PL games
    pl_events = [e for e in events if e['compid'] == '296']

    markets = {}

    #Loop through each PL game from lengjan
    for e in pl_events:
        odds = urllib.request.urlopen("https://games.lotto.is/game/lengjan-markets?live=0&eventId=" + str(e['eventid'])).read()
        odds = json.loads(odds)
        odds = odds['markets']
        markets[e['eventid']] = {}
        markets[e['eventid']]['markets'] = []
        markets[e['eventid']]['participants'] = e['participants']
        markets[e['eventid']]['understat'] = []
        """print(games[0])
        print('++++++++++++++++++')
        print(odds[0])
        print("-----------------")"""
        

        #Loop through csOdds games
        for g in games:
            
            if(e['participants'][0]['name'][-1] == ' '):
                if g['team'] == lengjan_teams[e['participants'][0]['name'][:-1]]:
                    markets[e['eventid']]['understat'].append(g)
            else: 
                if g['team'] == lengjan_teams[e['participants'][0]['name']]:
                    markets[e['eventid']]['understat'].append(g)

            if(e['participants'][1]['name'][-1] == ' '):
                if g['team'] == lengjan_teams[e['participants'][1]['name'][:-1]]:
                    markets[e['eventid']]['understat'].append(g)
            else: 
                if g['team'] == lengjan_teams[e['participants'][1]['name']]:
                    markets[e['eventid']]['understat'].append(g)

        #
        for o in odds:
            if o['marketsubtype'] == '44' or o['marketsubtype'] == '43':
                markets[e['eventid']]['markets'].append({'marketname':o['marketname'],'selections':o['selections']})
    
        #filter out entries with no markets
        final_markets = {}
        for key in markets:
            if (markets[key]['understat'][1]['opponent'] == lengjan_teams[markets[key]['participants'][0]['name']] and
            markets[key]['understat'][0]['opponent'] == lengjan_teams[markets[key]['participants'][1]['name']] and
            markets[key]['markets'] != []):
                final_markets[key] = markets[key]
    

    with open('tempfiles/temp_clean_sheet_odds.json', 'w') as file:
        file.write(json.dumps(final_markets))

    try:
        with open('tempfiles/bet_scheme.json', 'r') as all_games:
            all_bets = json.load(all_games)
    except:
        all_bets = []
    

    bets_to_save = []
    
    markets = final_markets
    for key in markets:
        if markets[key]['markets'] != []:
            home_team = markets[key]['understat'][0]['team']
            my_home_team_odds = str(markets[key]['understat'][0]['csOdds'])
            lengjan_home_team_odds = str(100 / float(markets[key]['markets'][0]['selections'][1]['odds']))

            my_home_concede_odds = str(1.0 - float(my_home_team_odds))
            lengjan_home_team_concede_odds = str(100 / float(markets[key]['markets'][0]['selections'][0]['odds']))

            #print(key)
            #print(markets[key]['understat'])
            away_team = markets[key]['understat'][1]['team']
            
            my_away_team_odds = str(markets[key]['understat'][1]['csOdds'])
            lengjan_away_team_odds = str(100 / float(markets[key]['markets'][1]['selections'][1]['odds']))

            my_away_concede_odds = str(1.0 - float(my_away_team_odds))
            lengjan_away_team_concede_odds = str(100 / float(markets[key]['markets'][1]['selections'][0]['odds']))

            #Print out and save entries if our models odds are morer favorable than the odds of Lengjan
            if(float(my_home_team_odds) > float(lengjan_home_team_odds)):
                print('BET Clean Sheet(+' + str(round(100*(float(my_home_team_odds) - float(lengjan_home_team_odds)),2)) + '%): ' + home_team + ' against ' + away_team + ': ' + my_home_team_odds+ ' ' + lengjan_home_team_odds)
                #print(markets[key]['understat'])
                bets_to_save.append({'cS':'Yes','home_away':'home','team':home_team,'opponent':away_team,'myOdds':my_home_team_odds,'lengjanOdds':lengjan_home_team_odds,'fpl_code':markets[key]['understat'][0]['code'],'result':0})
            if((float(my_home_concede_odds) > float(lengjan_home_team_concede_odds))):
                print('BET NO Clean Sheet(+' + str(round(100*(float(my_home_concede_odds) - float(lengjan_home_team_concede_odds)),2))+ '%): ' + home_team + ' against ' + away_team + ': ' + my_home_concede_odds + ' ' + lengjan_home_team_concede_odds)
                #print(markets[key]['understat'])
                bets_to_save.append({'cS':'No','home_away':'home','team':home_team,'opponent':away_team,'myOdds':my_home_concede_odds,'lengjanOdds':lengjan_home_team_concede_odds,'fpl_code':markets[key]['understat'][0]['code'],'result':0})
            if(float(my_away_team_odds) > float(lengjan_away_team_odds)):
                print('BET Clean Sheet(+' + str(round(100*(float(my_away_team_odds) - float(lengjan_away_team_odds)),2)) + '%): ' + away_team + ' against ' + home_team + ': ' + my_away_team_odds+ ' ' + lengjan_away_team_odds)
                bets_to_save.append({'cS':'Yes','home_away':'away','team':away_team,'opponent':home_team,'myOdds':my_away_team_odds,'lengjanOdds':lengjan_away_team_odds,'fpl_code':markets[key]['understat'][0]['code'],'result':0})
                #print(markets[key]['understat'])
            if((float(my_away_concede_odds) > float(lengjan_away_team_concede_odds))):
                print('BET NO Clean Sheet(+' + str(round(100*(float(my_away_concede_odds) - float(lengjan_away_team_concede_odds)),2))+ '%): ' + away_team + ' against ' + home_team + ': ' + my_away_concede_odds + ' ' + lengjan_away_team_concede_odds)
                bets_to_save.append({'cS':'No','home_away':'away','team':away_team,'opponent':home_team,'myOdds':my_away_concede_odds,'lengjanOdds':lengjan_away_team_concede_odds,'fpl_code':markets[key]['understat'][0]['code'],'result':0})
                #print(markets[key]['understat'])
            
            
            final_bets_to_save = []
            for bet in bets_to_save:
                if bet not in all_bets:
                    final_bets_to_save.append(bet)

            if final_bets_to_save != []:
                with open('tempfiles/bet_scheme.json', 'w') as file:
                    file.write(json.dumps(all_bets + final_bets_to_save))