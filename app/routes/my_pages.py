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

            return {
                'person': {
                    'info': my_pages.person_info['vivadata'],
                    'cases': my_pages.person_cases['vivadata']
                }
            }, 200

        except Fault as fault:
            return {
                'fault': {
                    'message': fault.message,
                }
            }, 500
