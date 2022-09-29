from flask import current_app
from flask_restful import Resource

from app.libs.classes.viva_my_pages import VivaMyPages
from app.libs.personal_number_helper import hash_to_personal_number
from app.libs.authenticate_helper import authenticate

from app.data.users import USERS


class MyPages(Resource):
    method_decorators = [authenticate]

    def get(self, hash_id=None):

        if current_app.config['ENV'] in ['development', 'test']:
            if not hash_id:
                return {
                    'users': USERS
                }, 200

        return self._get_mypages_all_details(hash_id=hash_id)

    def _get_mypages_all_details(self, hash_id):
        personal_number = hash_to_personal_number(hash_id=hash_id)
        my_pages = VivaMyPages(user=personal_number)

        response = {
            'type': 'getMyPages',
            'attributes': {
                'cases': my_pages.person_cases['vivadata'],
            }
        }

        if my_pages.person_application is not False:
            response['attributes']['application'] = my_pages.person_application['vivadata']

        return response, 200
