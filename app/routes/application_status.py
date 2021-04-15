from flask_restful import Resource
from zeep.exceptions import Fault

from ..libs import VivaApplicationStatus
from ..libs import decode_hash_id
from ..errors import ValidationError


class ApplicationStatus(Resource):

    def get(self, hash_id):
        hash_id_tuple = decode_hash_id(hash_id=hash_id)

        if len(hash_id_tuple) == 0:
            raise ValidationError(
                message=f'The hashid {hash_id} in the url is not a valid hashid')

        personal_number = hash_id_tuple[0]

        if current_app.config['ENV'] in ['development', 'test']:
            personal_number = to_test_personal_number(personal_number)

        viva_application_status = VivaApplicationStatus(
            personal_number=personal_number)

        response = viva_application_status.get()

        return response, 200
