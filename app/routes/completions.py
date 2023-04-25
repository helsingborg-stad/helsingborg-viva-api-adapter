from flask import request
from flask_restful import Resource

from app.libs.enum import ApplicationType
from app.libs.providers.viva_abc_provider import AbstractVivaProvider
from app.libs.classes.viva_application_data import DataClassApplication
from app.libs.classes.viva_my_pages import VivaMyPages
from app.libs.classes.viva_attachments import VivaAttachments
from app.libs.classes.viva_application import VivaApplication
from app.libs.personal_number_helper import hash_to_personal_number
from app.libs.authenticate_helper import authenticate
from app.schemas.completion_schema import CompletionSchema


class Completions(Resource):
    method_decorators = [authenticate]

    def __init__(self, provider: AbstractVivaProvider) -> None:
        self.provider = provider

    def post(self, hash_id):
        json_payload = request.json

        personal_number = hash_to_personal_number(hash_id=hash_id)

        completion_schema = CompletionSchema()
        validated_completion_payload = completion_schema.load(json_payload)

        client = self.provider.create_client(
            wsdl_name='VivaApplication')

        my_pages = VivaMyPages(user=personal_number, client=self.provider.create_client(
            wsdl_name='MyPages'))

        viva_attachments = VivaAttachments(
            client=self.provider.create_client(wsdl_name='VivaAttachment'), user=personal_number)

        viva_application = VivaApplication(
            client=client,
            my_pages=my_pages,
            viva_attachments=viva_attachments,
            application=DataClassApplication(
                operation_type=ApplicationType.COMPLETION,
                attachments=validated_completion_payload['attachments'],
                workflow_id=validated_completion_payload['workflow_id']))

        return {
            'type': 'completions',
            'attributes': viva_application.submit(),
        }, 200
