from flask_restful import Resource
from zeep.exceptions import Fault

from ..libs import VivaApplicationStatus
from ..libs import hash_to_personal_number
from ..errors import ValidationError


class ApplicationStatus(Resource):

    def get(self, hash_id):
        if not len(hash_id) == 32:
            raise ValidationError(
                message=f'The hashid {hash_id} in the url is not a valid hashid')

        personal_number = hash_to_personal_number(hash_id=hash_id)
        print(personal_number)

        viva_application_status = VivaApplicationStatus(
            personal_number=personal_number)
        print(viva_application_status)

        response = viva_application_status.get()

        return response, 200
