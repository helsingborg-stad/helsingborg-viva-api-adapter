from flask import current_app, jsonify
from flask_restful import Resource, reqparse

from ..libs.viva_application import VivaApplication

parser = reqparse.RequestParser()
parser.add_argument('type', required=True)
parser.add_argument('body', type=dict, required=True)

class Applications(Resource):
    def get(self):
        return 'APPLICATIONS'

    def post(self):
        json_data = parser.parse_args()

        vivaAppli = VivaApplication(
            usr='19760819T1234',
            pnr='19760819T1234'
        )

        response = vivaAppli.new_re_application(
            key=123,
            period={},
            re_application={ 'some': 'value' }
        )

        return jsonify(response)
