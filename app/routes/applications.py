from flask import current_app, jsonify
from flask_restful import Resource, reqparse

from ..libs.viva_application import VivaApplication

parser = reqparse.RequestParser()
parser.add_argument('application_type', type=str, required=True)
parser.add_argument('user', type=str, required=True)
parser.add_argument('body', type=dict, required=True)


class Applications(Resource):
    def get(self):
        return 'APPLICATIONS'

    def post(self):
        json_data = parser.parse_args()
        appli_type = json_data.type

        usr = json_data.body.usr
        pnr = json_data.body.pnr

        viva_appli = VivaApplication(usr=usr, pnr=pnr)

        if appli_type == 'renew':

            renew_response = viva_appli.new_re_application(
                key=123,
                period={},
                re_application={'some': 'value'}
            )

            return jsonify(renew_response)

        elif appli_type == 'new':
            return jsonify(json_data)
