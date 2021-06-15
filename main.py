from flask import (
    Flask,
    render_template
)
from flask_restful import Resource, Api
import requests
import json
import logging
from ratelimit import limits, sleep_and_retry

app = Flask(__name__)
api = Api(app)

# Homepage
@app.route('/')
def home():
    return render_template('home.html')

# Instantiate logger
logging.getLogger(__name__)


class ApiHelper:
    def __init__(self):
        self.seasonStartYear = '2019'
        self.seasonEndYear = '2020'
        self.resultsPerPage = '40'

    def get_url(self, league):
        if league == 'Premier League':
            url = 'https://api.football-data.org/v2/competitions/PL/matches?season='\
                  +self.seasonStartYear+'&limit='+self.resultsPerPage
        elif league == 'NBA':
            url = 'https://www.balldontlie.io/api/v1/games?seasons[]='\
                  +self.seasonStartYear+'&per_page='+self.resultsPerPage
        logging.info('League: {}, Url: {}'.format(league, url))
        return url

    def get_results(self, url, apiKey):
        if apiKey is not None:
            headers = {'X-Auth-Token': apiKey, 'Content-Type': 'application/json'}
        else:
            headers = {'Content-Type': 'application/json'}
        resp = requests.get(url, headers=headers)
        logging.info('API Response: status code {}, content: {}'.format(resp.status_code, resp.content))
        return resp


class DataHandler:
    def format_premier_league_scores(self, data):
        logging.info('Formatting data.')
        jsonData = json.loads(data)
        matches = jsonData['matches']
        scoresList = []
        for match in matches:
            matchId = match['id']
            matchDate = match['utcDate']
            homeTeam = match['homeTeam']
            awayTeam = match['awayTeam']
            scoreData = match['score']
            matchData = {
                'matchId': matchId,
                'matchDate': matchDate,
                'homeTeam': homeTeam,
                'awayTeam': awayTeam,
                'score': scoreData
            }
            jsonMatchData = json.dumps(matchData)
            scoresList.append(jsonMatchData)
        return scoresList

    def format_nba_scores(self, data):
        logging.info('Formatting data.')
        jsonData = json.loads(data)
        matches = jsonData['data']
        scoresList = []
        for match in matches:
            matchId = match['id']
            matchDate = match['date']
            homeTeam = match['home_team']['full_name']
            awayTeam = match['visitor_team']['full_name']
            scoreData = {
                'home_team_score' : match['home_team_score'],
                'away_team_score': match['visitor_team_score']
            }
            matchData = {
                'matchId': matchId,
                'matchDate': matchDate,
                'homeTeam': homeTeam,
                'awayTeam': awayTeam,
                'score': scoreData
            }
            jsonMatchData = json.dumps(matchData)
            scoresList.append(jsonMatchData)
        return scoresList



# Test
a = ApiHelper()
d = DataHandler()
url = a.get_url('Premier League')
apikey = '938f39c800744f9dbff8e8948491f65d'
footballResp = a.get_results(url, apikey)
formattedData = d.format_premier_league_scores(footballResp.content)
print(formattedData)

urlb = a.get_url('NBA')
print(urlb)
basketballResp = a.get_results(urlb, None)
formattedDataB = d.format_nba_scores(basketballResp.content)
print(formattedDataB)
