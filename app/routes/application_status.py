from flask_restful import Resource
from flask import current_app
from zeep.exceptions import Fault

from ..libs import VivaApplicationStatus
from ..libs import hash_to_personal_number
from ..errors import CustomValidationError


class ApplicationStatus(Resource):

    def get(self, hash_id):
        personal_number = hash_to_personal_number(hash_id=hash_id)

        viva_application_status = VivaApplicationStatus(
            personal_number=personal_number)

        response = viva_application_status.get()

        return response, 200
