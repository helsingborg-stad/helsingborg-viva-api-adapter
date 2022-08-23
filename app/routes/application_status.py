from flask_restful import Resource

from app.libs.classes.viva_application_status import VivaApplicationStatus
from app.libs.personal_number_helper import hash_to_personal_number
from app.libs.authenticate_helper import authenticate


class ApplicationStatus(Resource):
    method_decorators = [authenticate]

    def get(self, hash_id):
        personal_number = hash_to_personal_number(hash_id=hash_id)

        viva_application_status = VivaApplicationStatus(
            personal_number=personal_number)

        response = viva_application_status.get()

        return response, 200
