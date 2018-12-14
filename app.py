import logging
import sys
import requests
from flask import Flask, render_template, redirect, url_for, request, session, flash, g, abort, Blueprint, jsonify
from flask_restplus import Api, Resource, fields
import zipcodes
import json

app = Flask(__name__)


api_v1 = Blueprint('api', __name__, url_prefix='/api/1')

api = Api(api_v1, version='1.0', title='ADX Zip-code Microservice',
    description='A Dockerized Zipcode Micro-service built for the ADX3 PaaS',
)

ns = api.namespace('zipcode', description='Did You Know?! The term ZIP is an acronym for Zone Improvement Plan')


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
        abort_if_todo_doesnt_exist(zipcode_id)
        return zipcodes.matching(str(zipcode_id))
        #return zipcodes.matching(str(zipcode_id))

def get_coords(zipcode, map_connection_string="http://10.0.5.11:8880"):
    """
    """
    url = map_connection_string + "/api/1/zipcode/" + str(zipcode)
    response = requests.get(url=url)
    loc_map = response.json()[0]
    return loc_map['lat'], loc_map['long'], response.text


@app.route('/', methods=['GET', 'POST']) #this is called a decorator
def home():
    map_url = "10.0.5.11:8002"
    map_style = "osm-bright"
    lat = "36.67"
    long = "-76.3"
    loc_json = "empty"

    if request.method == 'POST':
        if request.form['zipcode']:
            zip_code = request.form['zipcode']
            lat, long, loc_json = get_coords(zip_code)
#            application.logger.info('[Moo] '+ unicode(now.replace(microsecond=0)) + "\t" + request.remote_addr + "\t" + moo_text)
    return render_template("index.html", map_url=map_url,map_style=map_style, lat=lat, long=long, loc_json = loc_json)

@app.route('/dark', methods=['GET', 'POST']) #this is called a decorator
def home2():
    map_url = "10.0.5.11:8002"
    map_style = "osm-bright"
    lat = "36.67"
    long = "-76.3"
    loc_json = "empty"

    if request.method == 'POST':
        if request.form['zipcode']:
            zip_code = request.form['zipcode']
            lat, long, loc_json = get_coords(zip_code)
#            application.logger.info('[Moo] '+ unicode(now.replace(microsecond=0)) + "\t" + request.remote_addr + "\t" + moo_text)
    return render_template("dark.html", map_url=map_url,map_style=map_style, lat=lat, long=long, loc_json = loc_json)

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
    app.run(port=8880,debug=True, host="0.0.0.0")

    #http://localhost:8080/styles/klokantech-basic/#12.61/38.92915/-77.22274
