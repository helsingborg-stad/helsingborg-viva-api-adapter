from flask_restful import Resource
from zeep.exceptions import Fault

from ..libs import VivaApplicationStatus
from ..libs import hash_to_personal_number


class ApplicationStatus(Resource):

    def get(self, hash_id):
        try:
            if not hash_id:
                raise TypeError('hash_id should be type string')

            personal_number = hash_to_personal_number(hash_id=hash_id)

            viva_application_status = VivaApplicationStatus(
                personal_number=personal_number)

            response = viva_application_status.get()

            return response, 200

        except Fault as fault:
            return {
                'message': fault.message,
                'code': fault.code,
            }, fault.code

        except Exception as error:
            return {
                'message': f'{error}',
                'code': 500,
            }, 500
