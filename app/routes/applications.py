from flask import jsonify, request, current_app
from flask_restful import Resource
from marshmallow import ValidationError

from ..libs import VivaApplication, decode_hash_personal_number, make_test_personal_number, parse_application_data
from ..schemas import ApplicationSchema, ResponseSchema


class Applications(Resource):
    def get(self):
        return 'APPLICATIONS LIST'

    def post(self):
        json_payload = request.json

        application_schema = ApplicationSchema()

        try:
            application_data = application_schema.load(json_payload)
        except ValidationError as error:
            return jsonify(error.messages)

        parsed_application_data = parse_application_data(
            answers=application_data['answers'],
            period=application_data['period'],
            initial_data={
                'RAWDATA': '',
                'RAWDATATYPE': 'PDF',
                'HOUSEHOLDINFO': '',
                'OTHER': ''
            }
        )

        personal_number = decode_hash_personal_number(
            hash_id=application_data['applicant'])

        if current_app.config['ENV'] == 'development' or current_app.config['ENV'] == 'test':
            personal_number = make_test_personal_number(personal_number)

        application = VivaApplication(
            application_type=application_data['application_type'],
            application_data=parsed_application_data,
            personal_number=personal_number,
            client_ip=application_data['client_ip'],
            workflow_id=application_data['workflow_id'],
            period=application_data['period'],
        )

        response = application.create()

        response_schema = ResponseSchema()
        try:
            validated_response = response_schema.load(response)
            return validated_response
        except ValidationError as error:
            return jsonify(error.messages)
