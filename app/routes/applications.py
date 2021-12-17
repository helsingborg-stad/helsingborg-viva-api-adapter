from flask import request
from flask_restful import Resource

from ..libs import DataClassApplication
from ..libs import VivaMyPages
from ..libs import VivaApplication
from ..libs import hash_to_personal_number
from ..libs import authenticate

from ..schemas import ApplicationSchema


class Applications(Resource):
    method_decorators = [authenticate]

    def post(self):
        json_payload = request.json

        application_schema = ApplicationSchema()
        validated_application = application_schema.load(json_payload)

        personal_number = hash_to_personal_number(
            hash_id=validated_application['hashid'])

        viva_application = VivaApplication(
            my_pages=VivaMyPages(user=personal_number),
            application=DataClassApplication(
                operation_type=validated_application['application_type'],
                workflow_id=validated_application['workflow_id'],
                answers=validated_application['answers'],
                raw_data=validated_application['raw_data']))

        response = viva_application.submit()

        return response
