from flask import jsonify, request, current_app
from flask_restful import Resource
from marshmallow import ValidationError

from ..libs import VivaApplication
from ..libs import get_personal_number
from ..libs import authenticate

from ..schemas import ApplicationSchema, ResponseSchema


class Applications(Resource):
    method_decorators = [authenticate]

    def post(self):
        json_payload = request.json

        application_schema = ApplicationSchema()

        try:
            validated_payload = application_schema.load(json_payload)
        except ValidationError as error:
            return jsonify(error.messages)

        viva_application_instance = VivaApplication(
            application_type=validated_payload['application_type'],
            personal_number=get_personal_number(
                hash_id=validated_payload['hashid']),
            answers=validated_payload['answers']
        )

        response = viva_application_instance.create()

        response_schema = ResponseSchema()
        try:
            validated_response = response_schema.load(response)
            return validated_response
        except ValidationError as error:
            return jsonify(error.messages)
