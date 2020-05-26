from flask import Flask,render_template
import requests
import jinja2
#TODO add riot key
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

@app.route('/',methods['GET','POST'])
def index():
    return render_template('layout.html.jinja')

@app.route('/summoner/<summoner_name>',methods['GET'])
def summoner(summoner_name):

    return render_template('summoner.html')
if __name__ == '__main__':
    import os
    HOST = os.environ.get('SERVER_HOST', 'localhost')
    try:
        PORT = int(os.environ.get('SERVER_PORT', '5555'))
    except ValueError:
        PORT = 5555
    app.run(HOST, PORT)
