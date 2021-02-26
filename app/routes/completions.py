from flask import jsonify, request
from flask_restful import Resource
from zeep.exceptions import Fault
from marshmallow import ValidationError

from ..libs import VivaMyPages
from ..libs import VivaAttachments
from ..libs import VivaApplication
from ..libs import hash_to_personal_number
from ..libs import authenticate

from ..schemas import CompletionSchema
from ..schemas import ResponseSchema
from ..schemas import AttachmentsSchema


class Completions(Resource):
    method_decorators = [authenticate]

    def post(self, hash_id):
        try:
            json_payload = request.json

            completion_schema = CompletionSchema()
            validated_completion_payload = completion_schema.load(json_payload)

            validated_completion_payload['application_type'] = 'completion'

            personal_number = hash_to_personal_number(hash_id=hash_id)

            viva_application = VivaApplication(
                my_pages=VivaMyPages(user=personal_number),
                viva_attachments=VivaAttachments(user=personal_number),
                application=validated_completion_payload)

            submit_response = viva_application.submit()

            response_schema = ResponseSchema()
            validated_response = response_schema.load(submit_response)

            return validated_response

        except (ValidationError, Fault) as error:
            return jsonify(error.messages)
