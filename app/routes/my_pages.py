from flask_restful import Resource
from zeep.exceptions import Fault

from .. import data
from ..libs.hashids import parse_hash
from ..libs.my_pages import MyPages as VivaMyPages


class MyPages(Resource):
    def get(self, hash_id=None):

        if not hash_id:
            return {
                'users': data.USERS
            }

        try:
            user = parse_hash(hashid=hash_id)
            my_pages = VivaMyPages(user=user)

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
