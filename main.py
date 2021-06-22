from flask import Flask, render_template, jsonify
from flask_restful import Api
from get_scores import ApiHelper

app = Flask(__name__)
app.config["DEBUG"] = True
api = Api(app)


# Homepage
@app.route('/', methods=['GET'])
def home():
    return render_template('home.html')


@app.route('/api/v1/scores/<league>', methods=['GET'])
def result(league):
    apiHelper = ApiHelper()
    return jsonify(apiHelper.get_scores(league))


app.run()
