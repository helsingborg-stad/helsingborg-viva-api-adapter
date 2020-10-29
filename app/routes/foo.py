from flask import jsonify, request
from flask_restful import Resource
from marshmallow import ValidationError

from ..schemas import ApplicationSchema
from ..libs import parse_application_data, decode_hash_personal_number


class Foo(Resource):
    def post(self):
        json_payload = request.json

        application_schema = ApplicationSchema()

        try:
            application_data = application_schema.load(json_payload)
        except ValidationError as error:
            return jsonify(error.messages)

        initial_application_data = {
            'RAWDATA': '',
            'RAWDATATYPE': 'PDF',
            'HOUSEHOLDINFO': '',
            'OTHER': ''
        }

        parsed_application_data = parse_application_data(
            answers=application_data['answers'],
            period=application_data['period']
        )

        if not parsed_application_data:
            return {
                'error': 'No data'
            }, 400

        return {**initial_application_data, **parsed_application_data}, 200
