import urllib
import logging
import configparser
import sys
from openpyxl import load_workbook
from Strava import token_exchange
from TrainingSpreadsheet import Calandar, get_training_plan
from flask import Flask, request, session, redirect, render_template
from flask_session import Session


logging.basicConfig(filename="app.log", level=logging.DEBUG)

config = configparser.ConfigParser()
config.read("config.ini")

workbook = load_workbook(config['training plan']['Spreadsheet'])

app = Flask(__name__)
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_PERMANENT'] = False
app.secret_key = config['flask']['SecretKey']
Session(app)


@app.route("/")
def index():
    return "<a href=\"/authorize\">authorize</a>"


# Redirect to Strava OAuth
@app.route("/authorize", methods=['GET'])
def authorize_strava():
    params = {
        'client_id': config['strava']['ClientID'],
        'redirect_uri': "http://jordancameron.co.uk/token",
        'response_type': "code",
        'scope': "read_all"
    }
    return redirect('https://www.strava.com/oauth/authorize?{}'.format(urllib.parse.urlencode(params)))


# Run token exchange to get athletes auth info
@app.route("/token")
def token():
    code = request.args.get('code')
    # Todo: Store auth somewhere
    auth = token_exchange(config['strava']['ClientID'], config['strava']['ClientSecret'], code)
    return redirect('/')


@app.route("/training")
def training_spreadsheet():
    return render_template("RunTraining.html", training_plan_list=workbook.sheetnames)


@app.route("/training/<name>")
def training_plan(name):
    training_plan = get_training_plan(workbook, name)
    return render_template("RunTraining.html", calandar=Calandar(training_plan))


@app.route("/shutdown")
def shutdown():
    sys.exit()