from flask_restful import Resource
from flask import current_app
from zeep.exceptions import Fault

from ..libs import VivaApplicationStatus
from ..libs import decode_hash_id
from ..errors import CustomValidationError


class ApplicationStatus(Resource):

    def get(self, hash_id):
        decoded_hash_id = decode_hash_id(hash_id=hash_id)

        if len(decoded_hash_id) == 0:
            raise CustomValidationError(
                message=f'The server cannot or will not process the request due to something that is perceived to be a client error (e.g., malformed request syntax, invalid request message framing, or deceptive request routing).')

        personal_number = decoded_hash_id[0]

        if current_app.config['ENV'] in ['development', 'test']:
            personal_number = to_test_personal_number(personal_number)

        viva_application_status = VivaApplicationStatus(
            personal_number=personal_number)

        response = viva_application_status.get()

        return response, 200
