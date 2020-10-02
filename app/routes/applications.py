from flask import jsonify, request, current_app
from marshmallow import ValidationError
from flask_restful import Resource

from ..libs import VivaApplication, decode_hash_personal_number, make_test_personal_number, parse_application_data
from ..schemas import ApplicationSchema, ResponseSchema


class Applications(Resource):
    def get(self):
        return 'APPLICATIONS LIST'

    def post(self):
        json_payload = request.json

        application_schema = ApplicationSchema()
        try:
            validated_data = application_schema.load(json_payload)
        except ValidationError as error:
            return jsonify(error.messages)

        application_data = parse_application_data(
            data=validated_data['application_body'],
            period=validated_data['period'],
            initial_data={
                'RAWDATA': '',
                'RAWDATATYPE': 'PDF',
                'HOUSEHOLDINFO': '',
                'OTHER': ''
            }
        )

        personal_number = decode_hash_personal_number(
            hash_id=validated_data['personal_number'])

        if current_app.config['ENV'] == 'development' or current_app.config['ENV'] == 'test':
            personal_number = make_test_personal_number(personal_number)

        application = VivaApplication(
            application_type=validated_data['application_type'],
            application_data=application_data,
            personal_number=personal_number,
            client_ip=validated_data['client_ip'],
            workflow_id=validated_data['workflow_id'],
            period=validated_data['period'],
        )

        response = application.create()

        response_schema = ResponseSchema()
        try:
            validated_response = response_schema.load(response)
            return validated_response
        except ValidationError as error:
            return jsonify(error.messages)
