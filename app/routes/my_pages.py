from functools import wraps
from flask import current_app
from flask_restful import Resource
from zeep.exceptions import Fault

from ..libs import VivaMyPages
from ..libs import hash_to_personal_number, decode_hash_id, to_test_personal_number
from ..errors import CustomValidationError

from .. import data


def hash_id_to_personal_number(f):
    """
    Decorator function to validate token on route resources

    Example:
    class Applications(Resource):
        method_decorators = [validate_hash_id]
        ...
        ...
    """
    @wraps(f)
    def wrapper(*args, **kwargs):
        validation_error = CustomValidationError(
            message='The server cannot or will not process the request due to something that is perceived to be a client error (e.g., malformed request syntax, invalid request message framing, or deceptive request routing).')

        hash_id = kwargs.get('hash_id')
        if not hash_id:
            raise validation_error

        decoded_hash_id = decode_hash_id(hash_id=hash_id)

        if len(decoded_hash_id) == 0:
            raise validation_error

        personal_number = str(decoded_hash_id[0])

        if current_app.config['ENV'] in ['development', 'test']:
            personal_number = to_test_personal_number(personal_number)

        return f(personal_number=personal_number, *args, **kwargs)

    return wrapper


class MyPages(Resource):
    method_decorators = [hash_id_to_personal_number]

    def get(self, hash_id=None, personal_number=None):
        my_pages = VivaMyPages(user=personal_number)
        response = {
            'person': {
                'cases': my_pages.person_cases['vivadata'],
            }
        }

        if my_pages.person_application is not False:
            response['person']['application'] = my_pages.person_application['vivadata']

        return response, 200
