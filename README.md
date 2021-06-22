### Sports Results API

#### How to Use
- Homepage: http://localhost:5000/
- Go to http://localhost:5000/api/v1/scores/league_id to view scores
    - Premier League: http://localhost:5000/api/v1/scores/PL
    - NBA: http://localhost:5000/api/v1/scores/NBA
- NB: On line 25 of main.py, you will need to add your own API key
    - (It would be poor security practice to commit plaintext API key to GitHub)

#### Objectives
- Get match scores data for the following leagues:
    - Premier League
    - NBA
- Collate the data into a single dataset
- Serve the scores via a REST-ful endpoint
- Make it easy to add additional sports results APIs

#### TODO
- [ ] Collate the data into a single dataset to be queried
    - E.g. could periodically pull this data into SQL, then query relevant data with a stored proc
        - i.e. data flow would be: various APIs -> SQL database -> REST-ful endpoint
- [ ] Add pagination support for football-data API (Premier League)
- [ ] Make it possible to query results on a given date
- [ ] Nicer way of including API key
