from flask import jsonify, request, current_app
from flask_restful import Resource
from marshmallow import ValidationError

from ..libs import VivaApplication, personal_number_from_hash, make_test_personal_number, parse_application
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

        parsed_application = parse_application(
            answers=validated_data['answers'],
            period=validated_data['period']
        )

        personal_number = personal_number_from_hash(
            hash_id=validated_data['personal_number'])

        if current_app.config['ENV'] == 'development' or current_app.config['ENV'] == 'test':
            personal_number = make_test_personal_number(personal_number)

        application = VivaApplication(
            application_type=validated_data['application_type'],
            data={
                'client_ip': validated_data['client_ip'],
                'workflow_id': validated_data['workflow_id'],
                'period': validated_data['period'],
                'personal_number': personal_number,
                'application': parsed_application,
            }
        )

        response = application.create()

        response_schema = ResponseSchema()
        try:
            validated_response = response_schema.load(response)
            return validated_response
        except ValidationError as error:
            return jsonify(error.messages)
