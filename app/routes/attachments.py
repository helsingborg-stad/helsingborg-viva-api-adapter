from flask import request
from flask_restful import Resource

from app.libs.providers.viva_abc_provider import AbstractVivaProvider
from app.libs.classes.viva_attachments import VivaAttachments
from app.libs.personal_number_helper import hash_to_personal_number
from app.libs.authenticate_helper import authenticate
from app.schemas.attachments_schema import AttachmentsSchema


class Attachments(Resource):
    method_decorators = [authenticate]

    def __init__(self, provider: AbstractVivaProvider) -> None:
        self.provider = provider

    def post(self):
        json_payload = request.json

        attachments_schema = AttachmentsSchema()
        validated_attachment = attachments_schema.load(json_payload)

        personal_number = hash_to_personal_number(
            hash_id=validated_attachment['hashid'])

        client = self.provider.create_client(
            wsdl_name='VivaAttachment')

        viva_attachments = VivaAttachments(
            client=client, user=personal_number)

        save_result = viva_attachments.save(
            attachment=validated_attachment)

        return save_result, 200
