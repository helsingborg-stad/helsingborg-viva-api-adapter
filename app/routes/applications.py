from flask import request
from flask_restful import Resource

from ..libs import DataClassApplication
from ..libs import VivaMyPages
from ..libs import VivaAttachments
from ..libs import VivaApplication
from ..libs import hash_to_personal_number
from ..libs import authenticate

from ..schemas import ApplicationSchema


class Applications(Resource):
    method_decorators = [authenticate]

    def post(self):
        json_payload = request.json

        application_schema = ApplicationSchema()
        self.validated_application = application_schema.load(json_payload)

        self.personal_number = hash_to_personal_number(
            hash_id=self.validated_application['hashid'])

        application_type = self.validated_application['application_type']

        if application_type == 'new':
            return self._new_appliacation()

        return self._recurring_application()

    def _recurring_application(self):
        viva_recurring_application = VivaApplication(
            my_pages=VivaMyPages(user=self.personal_number),
            application=DataClassApplication(
                operation_type=self.validated_application['application_type'],
                personal_number=self.personal_number,
                workflow_id=self.validated_application['workflow_id'],
                answers=self.validated_application['answers'],
                raw_data=self.validated_application['raw_data']))

        return viva_recurring_application.submit()

    def _new_appliacation(self):
        viva_new_application = VivaApplication(
            viva_attachments=VivaAttachments(user=self.personal_number),
            application=DataClassApplication(
                operation_type='new',
                attachments=self.validated_application['attachments'],
                personal_number=self.personal_number,
                answers=self.validated_application['answers'],
                raw_data=self.validated_application['raw_data']))

        return viva_new_application.submit()
