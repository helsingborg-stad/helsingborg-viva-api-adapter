from flask_restful import Resource
from zeep.exceptions import Fault

from ..libs import MyPages as VivaMyPages
from ..libs import hash_to_personal_number

from .. import data


class MyPages(Resource):
    def get(self, hash_id=None):

        if not hash_id:
            return {
                'users': data.USERS
            }

        try:
            personal_number = hash_to_personal_number(hash_id=hash_id)
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
