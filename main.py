from flask import Flask
from flask_restful import Resource, Api
import requests
import json
# import logging
from ratelimit import limits, sleep_and_retry

app = Flask(__name__)
app.config["DEBUG"] = True
api = Api(app)


# Homepage
@app.route('/', methods=['GET'])
def home():
    return "<h1>Sports Results API | Home Page</h1>"


@app.route('/api/v1/scores', methods=['GET', 'POST'])
def results():
    return 'temp'


# app.run()


# # TODO: Change print to logging
# # Instantiate logger
# logging.getLogger(__name__)
# logging.basicConfig(format='%(asctime)s:%(message)s', level=logging.DEBUG)


# For rate limits
MAX_REQUESTS_PL = 10
MAX_REQUESTS_NBA = 60
ONE_MINUTE = 60


class ApiHelper:
    # TODO: make these user inputs
    def __init__(self):
        self.seasonStartYear = '2019'
        self.seasonEndYear = '2020'
        self.resultsPerPage = '40'

    @sleep_and_retry
    @limits(calls=MAX_REQUESTS_PL, period=ONE_MINUTE)
    def get_premier_league_scores(self, apiKey):
        url = 'https://api.football-data.org/v2/competitions/PL/matches?season=' \
              + self.seasonStartYear + '&limit=' + self.resultsPerPage
        print('League: Premier League, Url: {}'.format(url))
        headers = {'X-Auth-Token': apiKey, 'Content-Type': 'application/json'}
        resp = requests.get(url, headers=headers)
        print('API Response: status code {}, content: {}'.format(resp.status_code, resp.content))
        return resp

    @sleep_and_retry
    @limits(calls=MAX_REQUESTS_NBA, period=ONE_MINUTE)
    def get_nba_scores(self, maxPages):
        scoresList = []
        d = DataHandler()
        for n in range(1, maxPages):
            url = 'https://www.balldontlie.io/api/v1/games?seasons[]=' \
                  + self.seasonStartYear + '&per_page=' + self.resultsPerPage + '&page=' + str(n)
            print('League: NBA, Url: {}'.format(url))
            headers = {'Content-Type': 'application/json'}
            resp = requests.get(url, headers=headers)
            print('API Response: status code {}, content: {}'.format(resp.status_code, resp.content))
            # If content is returned, format it and add it to the scores list
            # If not, break - we've reached the end of the results
            if (resp.content):
                scoresList.append(d.format_nba_scores(resp.content))
            else:
                break
        return scoresList


class DataHandler:
    def format_premier_league_scores(self, data):
        print('Formatting data.')
        jsonData = json.loads(data)
        matches = jsonData['matches']
        scoresList = []

        def handle_match_data(match):
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

        list(map(handle_match_data, matches))

        return scoresList

    def format_nba_scores(self, data):
        print('Formatting data.')
        jsonData = json.loads(data)
        matches = jsonData['data']
        scoresList = []

        def handle_match_data(match):
            matchId = match['id']
            matchDate = match['date']
            homeTeam = match['home_team']['full_name']
            awayTeam = match['visitor_team']['full_name']
            scoreData = {
                'home_team_score': match['home_team_score'],
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

        list(map(handle_match_data, matches))

        return scoresList



# Test
a = ApiHelper()
d = DataHandler()
# apikey = ''
# footballResp = a.get_premier_league_scores(apikey)
# formattedData = d.format_premier_league_scores(footballResp.content)
# print(formattedData)

basketballResp = a.get_nba_scores(3)
print(basketballResp)
