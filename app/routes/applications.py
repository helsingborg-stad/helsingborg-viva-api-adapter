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
from app.schemas.application_schema import ApplicationSchema


class Applications(Resource):
    method_decorators = [authenticate]

    def __init__(self, provider: AbstractVivaProvider) -> None:
        self.provider = provider

    def post(self):
        json_payload = request.json

        application_schema = ApplicationSchema()
        self.validated_application = application_schema.load(json_payload)

        self.personal_number = hash_to_personal_number(
            hash_id=self.validated_application['hashid'])

        application_type = self.validated_application['application_type']

        if application_type == ApplicationType.NEW.value:
            return self._new_application().submit()

        return {
            'type': 'postApplication',
            'attributes': self._recurring_application().submit(),
        }

    def _recurring_application(self) -> VivaApplication:

        client = self.provider.create_client(
            wsdl_name='VivaApplication')

        my_pages = VivaMyPages(user=self.personal_number, client=self.provider.create_client(
            wsdl_name='MyPages'))

        viva_attachments = VivaAttachments(
            client=self.provider.create_client(wsdl_name='VivaAttachment'), user=self.personal_number)

        return VivaApplication(
            client=client,
            my_pages=my_pages,
            application=DataClassApplication(
                operation_type=ApplicationType.RECURRING,
                personal_number=self.personal_number,
                workflow_id=self.validated_application['workflow_id'],
                answers=self.validated_application['answers'],
                raw_data=self.validated_application['raw_data']),
            viva_attachments=viva_attachments)

    def _new_application(self) -> VivaApplication:
        return VivaApplication(
            viva_attachments=VivaAttachments(user=self.personal_number),
            application=DataClassApplication(
                operation_type=ApplicationType.NEW,
                personal_number=self.personal_number,
                attachments=self.validated_application.get('attachments', []),
                answers=self.validated_application['answers'],
                raw_data=self.validated_application['raw_data']))
