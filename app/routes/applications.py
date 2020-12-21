from flask import jsonify, request
from flask_restful import Resource
from zeep.exceptions import Fault
from marshmallow import ValidationError

from ..libs import MyPages
from ..libs import VivaApplication
from ..libs import hash_to_personal_number
from ..libs import authenticate

from ..schemas import ApplicationSchema, ResponseSchema


class Applications(Resource):
    method_decorators = [authenticate]

    def get(self, hash_id=None):
        try:
            personal_number = hash_to_personal_number(hash_id=hash_id)

            viva_application = VivaApplication(
                my_pages=MyPages(user=personal_number))

            response = viva_application.get_application_status()

            return response, 200

        except Fault as fault:
            return {
                'message': fault.message,
                'code': fault.code
            }, fault.code

    def post(self):
        json_payload = request.json

        application_schema = ApplicationSchema()

        try:
            validated_payload = application_schema.load(json_payload)
        except ValidationError as error:
            return jsonify(error.messages)

        personal_number = hash_to_personal_number(
            hash_id=validated_payload['hashid'])

        viva_application = VivaApplication(
            application_type=validated_payload['application_type'],
            my_pages=MyPages(user=personal_number),
            answers=validated_payload['answers'])

        response = viva_application.submit()

        response_schema = ResponseSchema()
        try:
            validated_response = response_schema.load(response)
            return validated_response
        except ValidationError as error:
            return jsonify(error.messages)
