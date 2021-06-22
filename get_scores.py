import requests
import json
# import logging
from ratelimit import limits, sleep_and_retry

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
        self.resultsPerPage = 40
        self.maxPages = 3
        self.apiKeyPL = ''

    def get_scores(self, league):
        scores = []
        if (league == 'NBA'):
            scores = self.get_nba_scores(self.maxPages)
        elif (league == 'PL'):
            # TODO: Add pagination support here
            scores = self.get_premier_league_scores()
        return scores

    @sleep_and_retry
    @limits(calls=MAX_REQUESTS_PL, period=ONE_MINUTE)
    def get_premier_league_scores(self):
        scoresList = []
        url = 'https://api.football-data.org/v2/competitions/PL/matches?season=' \
              + self.seasonStartYear + '&limit=' + str(self.resultsPerPage)
        print('League: Premier League, Url: {}'.format(url))
        headers = {'X-Auth-Token': self.apiKeyPL, 'Content-Type': 'application/json'}
        resp = requests.get(url, headers=headers)
        print('API Response: status code {}, content: {}'.format(resp.status_code, resp.content))
        if (resp.content):
            d = DataHandler()
            scoresList = d.format_premier_league_scores(resp.content)
        return scoresList

    @sleep_and_retry
    @limits(calls=MAX_REQUESTS_NBA, period=ONE_MINUTE)
    def get_nba_scores(self, maxPages):
        scoresList = []
        d = DataHandler()
        for n in range(1, (maxPages + 1)):
            url = 'https://www.balldontlie.io/api/v1/games?seasons[]=' \
                  + self.seasonStartYear + '&per_page=' + str(self.resultsPerPage) + '&page=' + str(n)
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
