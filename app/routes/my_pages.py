from flask import current_app
from flask_restful import Resource, reqparse
from zeep.exceptions import Fault


from .. import data
from ..libs.my_pages import MyPages as VivaMyPages


class MyPages(Resource):
    def get(self, hash_id=None):

        if not hash_id:
            return {
                'users': data.USERS
            }

        try:
            my_pages = VivaMyPages(user_pnr_hashed=hash_id)

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
