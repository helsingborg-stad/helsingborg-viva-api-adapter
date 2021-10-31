from flask import current_app
from flask_restful import Resource
from zeep.exceptions import Fault

from ..libs import VivaMyPages

from ..libs import hash_to_personal_number
from ..libs import authenticate

from .. import data


class MyPages(Resource):
    method_decorators = [authenticate]

    def get(self, hash_id=None):

        if current_app.config['ENV'] in ['development', 'test']:
            if not hash_id:
                return {
                    'users': data.USERS
                }, 200

        return self._get_mypages_all_details(hash_id=hash_id)

    def _get_mypages_all_details(self, hash_id):
        try:
            personal_number = hash_to_personal_number(hash_id=hash_id)
            my_pages = VivaMyPages(user=personal_number)

            response = {
                'person': {
                    'cases': my_pages.person_cases['vivadata'],
                }
            }

            if my_pages.person_application is not False:
                response['person']['application'] = my_pages.person_application['vivadata']

            return response, 200

        except Fault as fault:
            return {
                'message': fault.message,
                'code': fault.code
            }, fault.code
