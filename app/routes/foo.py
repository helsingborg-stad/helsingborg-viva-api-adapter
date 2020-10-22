from flask import jsonify, request
from marshmallow import ValidationError
from flask_restful import Resource
from pprint import pprint

from ..schemas import ApplicationSchema
from ..libs import parse_application_data, decode_hash_personal_number


class Foo(Resource):
    def post(self):
        json_payload = request.json

        application_schema = ApplicationSchema()

        try:
            valid_application_data = application_schema.load(json_payload)
        except ValidationError as error:
            return jsonify(error.messages)

        initial_data = {
            'RAWDATA': '',
            'RAWDATATYPE': 'PDF',
            'HOUSEHOLDINFO': '',
            'OTHER': ''
        }

        period = valid_application_data['period']
        period_string = f"{period['start_date']} - {period['end_date']}"

        parsed_application_data = parse_application_data(
            answers=valid_application_data['answers'],
            period_string=period_string
        )

        return parsed_application_data, 200
