import logging
import sys
import requests
from flask import Flask, render_template, redirect, url_for, request, session, flash, g, abort, Blueprint, jsonify, session
from flask_restplus import Api, Resource, fields
import zipcodes
import json

app = Flask(__name__)
app.secret_key = 'You Will Never Guess'

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

def get_coords(zipcode, map_connection_string="http://localhost:8080"):
    """
    """
    url = map_connection_string + "/api/1/zipcode/" + str(zipcode)
    response = requests.get(url=url)
    loc_map = response.json()[0]
    return loc_map['lat'], loc_map['long'], response.text


@app.route('/', methods=['GET', 'POST']) #this is called a decorator
def home():
    map_url = "openmaptiles-server:80"
    map_style = "osm-bright"
    lat = "38.95"
    long = "-77.34"
    loc_json = ""
    display_logo = ""
    #zip_code="20191"
    zip_code = ""

    if 'theme' not in session:
        session['theme']='cosmo'

    theme_request = request.args.get('theme')
    if theme_request is not None:
        session['theme'] = theme_request


    if request.method == 'POST':
        if request.form['zipcode']:
            zip_code = request.form['zipcode']
            lat, long, loc_json = get_coords(zip_code)
            #display_logo = "display: none;"
#            application.logger.info('[Moo] '+ unicode(now.replace(microsecond=0)) + "\t" + request.remote_addr + "\t" + moo_text)
    return render_template("index.html", map_url=map_url,map_style=map_style, lat=lat, long=long, loc_json = loc_json, display_logo=display_logo, zip_code=zip_code, theme=session['theme'])

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
    app.run(port=8080,debug=True, host="0.0.0.0")

    #http://localhost:8080/styles/klokantech-basic/#12.61/38.92915/-77.22274
