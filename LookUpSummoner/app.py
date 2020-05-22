from flask import Flask
import requests
from math import ceil
riot_api_key = 'RGAPI-d094861d-a242-443c-b6b7-c485ea971ac8'

app = Flask(__name__)

servers = {
           'EUNE':'eun1',
           'EUW':'euw1',
           'NA':'na1'
           }

# Make the WSGI interface available at the top level so wfastcgi can get it.
wsgi_app = app.wsgi_app

def get_summoner_id(summonername,region):
    region_in_url = servers[region]
    URL = 'https://'+region_in_url+'.api.riotgames.com/lol/summoner/v4/summoners/by-name/'+summonername+'?api_key='+ riot_api_key
    response = requests.get(URL)
    summoner_information = response.json()
    summoner_id = summoner_information['id']
    return summoner_id

def get_ranked_info(summonerId,region):
    region_in_url = servers[region]
    URL = 'https://'+ region_in_url + '.api.riotgames.com/lol/league/v4/entries/by-summoner/'+ summonerId +'?api_key='+ riot_api_key
    response = requests.get(URL)
    ranked_info = response.json()
    ranked_tier = ranked_info[0]['tier']
    ranked_rank = ranked_info[0]['rank']
    ranked_points = ranked_info[0]['leaguePoints']
    ranked_wins = ranked_info[0]['wins']
    ranked_losses = ranked_info[0]['losses']
    ranked_games_count = ranked_wins+ranked_losses
    ranked_winratio = (ranked_wins/ranked_games_count)*100
    return 'You are a %s %s player with %d points with a  %d Winrate' % (ranked_tier,ranked_rank,ranked_points,ranked_winratio)

@app.route('/')
def hello():
    """Renders a sample page."""
    id = get_summoner_id('GinkoTHEKILLER','EUNE')
    return get_ranked_info(id,'EUNE')



if __name__ == '__main__':
    import os
    HOST = os.environ.get('SERVER_HOST', 'localhost')
    try:
        PORT = int(os.environ.get('SERVER_PORT', '5555'))
    except ValueError:
        PORT = 5555
    app.run(HOST, PORT)
