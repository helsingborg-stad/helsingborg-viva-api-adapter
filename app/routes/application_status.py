from flask_restful import Resource

from ..libs import VivaApplicationStatus
from ..libs import hash_to_personal_number
from ..libs import authenticate


class ApplicationStatus(Resource):
    method_decorators = [authenticate]

    def get(self, hash_id):
        personal_number = hash_to_personal_number(hash_id=hash_id)

        viva_application_status = VivaApplicationStatus(
            personal_number=personal_number)

        response = viva_application_status.get()

        return response, 200
