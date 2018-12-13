from flask import Flask, Blueprint
from flask_restplus import Api, Resource, fields
import zipcodes

api_v1 = Blueprint('api', __name__, url_prefix='/api/1')

api = Api(api_v1, version='1.0', title='ADX Zip-code Microservice',
    description='A Dockerized Zipcode Micro-service built for the ADX3 PaaS',
)

ns = api.namespace('zipcode', description='Did You Know?! The term ZIP is an acronym for Zone Improvement Plan')


def abort_if_todo_doesnt_exist(todo_id):
    if False:
        api.abort(404, "Todo {} doesn't exist".format(todo_id))

parser = api.parser()
#parser.add_argument('task', type=str, required=True, help='required zipcode', location='form')
#parser.add_argument('task', type=str, required=True, help='required zipcode', location='form')


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



if __name__ == '__main__':
    app = Flask(__name__)
    app.register_blueprint(api_v1)
    app.config['SWAGGER_UI_DOC_EXPANSION'] = "full"
    app.run(port=8880,debug=True)