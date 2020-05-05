from flask import current_app, jsonify
from flask_restful import Resource, reqparse

from ..libs.viva_application import VivaApplication

parser = reqparse.RequestParser()
parser.add_argument('application_type', type=str, required=True)
parser.add_argument('user', type=str, required=True)
parser.add_argument('body', type=dict, required=True)


class Applications(Resource):
    def get(self):
        return 'APPLICATIONS LIST'

    def post(self):
        json_payload = parser.parse_args()

        application = VivaApplication(
            application_type=json_payload.application_type,
            user=json_payload.user,
            application_data=json_payload.body
        )

        response = application.create()

        return jsonify(response)
