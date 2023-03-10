from flask import current_app
from flask_restful import Resource

from app.libs.personal_number_helper import hash_to_personal_number
from app.libs.authenticate_helper import authenticate
from app.libs.data_domain.ekb_provider import EkbProvider

from app.data.users import USERS


class MyPages(Resource):
    method_decorators = [authenticate]

    def __init__(self, ekb: EkbProvider) -> None:
        self.ekb = ekb

    def get(self, hash_id):
        if current_app.config['ENV'] in ['development', 'test'] and not hash_id:
            return {'users': USERS}, 200

        personal_number = hash_to_personal_number(hash_id=hash_id)

        return {
            'type': 'getMyPages',
            'attributes': self.ekb.get_mypages(personal_number)
        }, 200
