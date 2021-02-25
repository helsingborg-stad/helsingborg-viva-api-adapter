from flask import jsonify, request
from flask_restful import Resource
from zeep.exceptions import Fault
from marshmallow import ValidationError

from ..libs import hash_to_personal_number
from ..libs import authenticate

from ..schemas import CompletionSchema, ResponseSchema


class Completions(Resource):
    method_decorators = [authenticate]

    def post(self, hash_id=None):
        json_payload = request.json

        completion_schema = CompletionSchema()

        try:
            validated_completion_request = completion_schema.load(json_payload)
        except ValidationError as error:
            return jsonify(error.messages)

        personal_number = hash_to_personal_number(
            hash_id=hash_id)

        dummy_response = {
            'ERRORCODE': '400',
            'ERRORMESSAGE': 'TEST WORKS',
            'STATUS': '400',
            'IDENCLAIR': 'idenclear',
            'ID': 'IDIDIDIDIDIDIDIDID'
        }

        response_schema = ResponseSchema()
        try:
            validated_response = response_schema.load(dummy_response)
            return validated_response
        except ValidationError as error:
            return jsonify(error.messages)
