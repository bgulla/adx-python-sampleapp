import logging
import sys
import requests
from flask import Flask, render_template, redirect, url_for, request, session, flash, g, abort, Blueprint, jsonify, session
from flask_restplus import Api, Resource, fields
import zipcodes
import json
import os
import socket
from contextlib import closing

app = Flask(__name__)
app.secret_key = '027f4073-a5ae-4ec6-a7e2-d730435a5867'

api_v1 = Blueprint('api', __name__, url_prefix='/api/1')

api = Api(api_v1, version='1.0', title='ADX Zip-code Microservice',
    description='A Dockerized Zipcode Micro-service built for the ADX3 PaaS',
)

ns = api.namespace('zipcode', description='Did You Know?! The term ZIP is an acronym for Zone Improvement Plan')

# Global vars that need to die3
#map_url = "https://openmaptiles-server-arc-team.apps.adx.dicelab.net"  # oc set env <object-selection> KEY=VALUE
map_style = "osm-bright"
default_lat = "38.95"
default_long = "-77.34"
PROTOCOL = "http://"

# ENV-based vars
FLASK_PORT = int(os.getenv('FLASK_PORT', 8080))

MAP_API_PROTOCOL = os.getenv('MAP_API_PROTOCOL', 'http://')
MAP_API_URI = os.getenv('MAP_API_URI', 'localhost:8080')
ZIPCODE_API_URI = os.getenv('ZIPCODE_API_URI', 'localhost:8080')
SSL_ENABLED = os.getenv('SSL_ENABLED', 'false')
DEFAULT_THEME = os.getenv('DEFAULT_THEME', 'cosmos')
DISABLE_COMPONENT = "display:none;"
BLANK = ""

if SSL_ENABLED == "true":
    PROTOCOL = "https://"
else:
    PROTOCOL = "http://"

map_url = MAP_API_PROTOCOL + MAP_API_URI

def abort_if_todo_doesnt_exist(todo_id):
    if False:
        api.abort(404, "Todo {} doesn't exist".format(todo_id))


@ns.route('/<string:zipcode_id>')
#@api.doc(responses={404: 'Zip-code not found'}, params={'zipcode_id': 'The Zip-code'})
class Todo(Resource):
    '''Show a single todo item and lets you delete them'''
    @api.doc(description='US Zip-codes only in Integer format')
    def get(self, zipcode_id):
        '''Fetch a given resource'''
        abort_if_todo_doesnt_exist(zipcode_id) # Replace this with syntax checker
        return zipcodes.matching(str(zipcode_id))

def get_coords(zipcode, map_connection_string=ZIPCODE_API_URI):
    """
    """
    url = PROTOCOL + map_connection_string + "/api/1/zipcode/" + str(zipcode)
    app.logger.info("[API-call] "+ url)
    response = requests.get(url=url)
    loc_map = response.json()[0]
    return loc_map['lat'], loc_map['long'], response.text


def is_map_server_online():
    """

    :return:
    """
    return False
    host = MAP_API_URI.split(':')[0]
    port = int(MAP_API_URI.split(':')[1])

    with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as sock:
        if sock.connect_ex((host, port)) == 0:
            return True
        else:
            app.logger.info("[FATAL] Map server not online "+ MAP_API_URI)
            return False
    app.logger.info("[FATAL] Unable to check for Map Server Connectivity")
    return False

@app.route('/status', methods=['GET', 'POST']) #this is the meat
def healthcheck():
    return "HEALTHY"

@app.route('/', methods=['GET', 'POST']) #this is the meat 
def home():
    lat=default_lat
    long=default_long
    loc_json = BLANK
    zip_code = BLANK
    error_msg = BLANK
    theme_request = BLANK
    display_alert = DISABLE_COMPONENT
    display_error = DISABLE_COMPONENT

    # HERE'S THE DEMO
    break_the_app = "style='background-color:red;'"
    #break_the_app = ""

    if not session.has_key('theme'):
        session['theme'] = DEFAULT_THEME

    """if not is_map_server_online():
        display_error = BLANK
        error_msg = "Unable to connect to map server at ", MAP_API_URI
    else:
        display_error = DISABLE_COMPONENT
        error_msg = BLANK
    """

    #Check to see if we need to update the theme
    theme_request = request.args.get('theme')
    if theme_request is not None:
        session['theme'] = theme_request
        app.logger.info("[THEME] Setting current theme to: ", theme_request)

    if request.method == 'POST':
        if request.form['zipcode']:
            zip_code = request.form['zipcode']
            # Call the API to get the info on the requested zipcode.
            lat, long, loc_json = get_coords(zip_code)
            display_alert = BLANK
    return render_template("index.html", break_the_app=break_the_app, map_url=map_url, map_style=map_style, lat=lat, long=long, loc_json = loc_json, display_logo="", zip_code=zip_code, theme=session['theme'], display_alert=display_alert, display_error=display_error, error_msg=error_msg)

@app.before_first_request
def setup_logging():
    if not app.debug:
        # In production mode, add log handler to sys.stdout.
        app.logger.addHandler(logging.StreamHandler(stream=sys.stdout))
        app.logger.setLevel(logging.INFO)

if __name__ == '__main__':
    app.logger.addHandler(logging.StreamHandler(stream=sys.stdout))
    app.logger.setLevel(logging.INFO)
    # TODO: Copy logger from the other example
    app.register_blueprint(api_v1)
    app.config['SWAGGER_UI_DOC_EXPANSION'] = "full"

    CERT_FILE = os.getenv('CERT_FILE', '/secret/cert/zipcode-tls.crt')
    KEY_FILE = os.getenv('KEY_FILE', '/secret/cert/zipcode-tls.key')
    app.logger.info("[INIT] SSL_ENABLED: "+ SSL_ENABLED)
    app.logger.info("[INIT] CERT_FILE: " + CERT_FILE)
    app.logger.info("[INIT] KEY_FILE: "+ KEY_FILE)

    if not os.path.isfile(KEY_FILE) or not os.path.isfile(CERT_FILE):
        app.run(port=FLASK_PORT, debug=True, host="0.0.0.0")
    else:
        app.run(port=8443, ssl_context=(CERT_FILE, KEY_FILE), debug=True, host="0.0.0.0")
