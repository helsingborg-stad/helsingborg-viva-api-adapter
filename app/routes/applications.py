from flask import jsonify, request
from flask_restful import Resource
from zeep.exceptions import Fault
from marshmallow import ValidationError

from ..libs import DataClassApplication
from ..libs import VivaMyPages
from ..libs import VivaAttachments
from ..libs import VivaApplication
from ..libs import hash_to_personal_number
from ..libs import authenticate

from ..schemas import ApplicationSchema
from ..schemas import ResponseSchema


class Applications(Resource):
    method_decorators = [authenticate]

    def get(self, hash_id=None):
        try:
            personal_number = hash_to_personal_number(hash_id=hash_id)

            viva_application = VivaApplication(
                application=DataClassApplication(operation_type='status'),
                my_pages=VivaMyPages(user=personal_number))

            response = viva_application.submit()

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
            validated_application = application_schema.load(json_payload)
        except ValidationError as error:
            return jsonify(error.messages)

        personal_number = hash_to_personal_number(
            hash_id=validated_application['hashid'])

        viva_application = VivaApplication(
            application=validated_application, my_pages=VivaMyPages(user=personal_number))

        response = viva_application.submit()

        response_schema = ResponseSchema()
        try:
            validated_response = response_schema.load(response)
            return validated_response
        except ValidationError as error:
            return jsonify(error.messages)
