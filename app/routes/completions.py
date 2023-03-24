from flask import request
from flask_restful import Resource

from app.libs.enum import ApplicationType
from app.libs.classes.viva_application_data import DataClassApplication
from app.libs.classes.viva_my_pages import VivaMyPages
from app.libs.classes.viva_attachments import VivaAttachments
from app.libs.classes.viva_application import VivaApplication
from app.libs.personal_number_helper import hash_to_personal_number
from app.libs.authenticate_helper import authenticate
from app.schemas.completion_schema import CompletionSchema


class Completions(Resource):
    method_decorators = [authenticate]

    def post(self, hash_id):
        json_payload = request.json

        personal_number = hash_to_personal_number(hash_id=hash_id)

        completion_schema = CompletionSchema()
        validated_completion_payload = completion_schema.load(json_payload)

        viva_application = VivaApplication(
            my_pages=VivaMyPages(user=personal_number),
            viva_attachments=VivaAttachments(user=personal_number),
            application=DataClassApplication(
                operation_type=ApplicationType.COMPLETION,
                attachments=validated_completion_payload['attachments'],
                workflow_id=validated_completion_payload['workflow_id']))

        return {
            'type': 'postCompletions',
            'attributes': viva_application.submit(),
        }, 200
