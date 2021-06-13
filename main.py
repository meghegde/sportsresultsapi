from flask import (
    Flask,
    render_template
)
from flask_restful import Resource, Api
import requests
import json

app = Flask(__name__)
api = Api(app)

# Homepage
@app.route('/')
def home():
    return render_template('home.html')


class QueryData:
    def __init__(self):
        self.seasonStartYear = '2019'
        self.seasonEndYear = '2020'
        self.resultsPerPage = '40'

    def get_url(self, league):
        if league == 'Premier League':
            url = 'https://api.football-data.org/v2/competitions/PL/matches?season='\
                  +self.seasonStartYear+'&limit='+self.resultsPerPage
        elif league == 'NBA':
            url = 'https://www.balldontlie.io/api/v1/games/seasons=['\
                  +self.seasonStartYear+']&per_page='+self.resultsPerPage
        return url

    def get_results(self, url, apiKey):
        if apiKey is not None:
            headers = {'X-Auth-Token': apiKey, 'Content-Type': 'application/json'}
        else:
            headers = {'Content-Type': 'application/json'}
        resp = requests.get(url, headers=headers)
        return resp

    def format_football_scores(self, data):
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


class Results(Resource):
    def get_results(self, league):
        return {'hello': 'world'}


# Test
q = QueryData()
url = q.get_url('Premier League')
apikey = ''
footballResp = q.get_results(url, apikey)
formattedData = q.format_football_scores(footballResp.content)
print(formattedData)
