from flask import current_app
from flask_restful import Resource
from zeep.exceptions import Fault

from .. import data
from ..libs import personal_number_from_hash, make_test_personal_number
from ..libs import MyPages as VivaMyPages


class MyPages(Resource):
    def get(self, hash_id=None):

        if not hash_id:
            return {
                'users': data.USERS
            }

        try:
            personal_number = personal_number_from_hash(hash_id=hash_id)

            if current_app.config['ENV'] == 'development' or current_app.config['ENV'] == 'test':
                personal_number = make_test_personal_number(personal_number)

            my_pages = VivaMyPages(user=personal_number)

            response = {
                'person': {
                    'info': my_pages.person_info['vivadata'],
                    'cases': my_pages.person_cases['vivadata'],
                    'booked_payments': my_pages.person_booked_payments['vivadata'],
                }
            }

            if my_pages.person_caseworkflow is not False:
                response['person']['caseworkflow'] = my_pages.person_caseworkflow['vivadata']

            if my_pages.person_application is not False:
                response['person']['application'] = my_pages.person_application['vivadata']

            return response, 200

        except Fault as fault:
            return {
                'message': fault.message,
                'code': fault.code
            }, 500
