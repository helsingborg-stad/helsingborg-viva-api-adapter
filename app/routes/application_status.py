from flask_restful import Resource
from zeep.exceptions import Fault

from ..libs import VivaApplicationStatus
from ..libs import hash_to_personal_number


class ApplicationStatus(Resource):

    def get(self, hash_id=None):
        try:
            personal_number = hash_to_personal_number(hash_id=hash_id)

            viva_application_status = VivaApplicationStatus(
                personal_number=personal_number)

            response = viva_application_status.get()

            return response, 200

        except Fault as fault:
            error = dict({
                'code': 500,
                'message': 'Internal Server Error',
            })

            if fault.code:
                error['code'] = fault.code

            if fault.message:
                error['message'] = fault.message

            return error, error.get('code')
