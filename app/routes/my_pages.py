from flask import current_app
from flask_restful import Resource

from app.libs.personal_number_helper import hash_to_personal_number
from app.libs.authenticate_helper import authenticate
from app.libs.providers.ekb_abc_provider import EkbABCProvider

from app.data.users import USERS


class MyPages(Resource):
    method_decorators = [authenticate]

    def __init__(self, provider: EkbABCProvider) -> None:
        self.provider = provider

    def get(self, hash_id) -> tuple:
        if not hash_id and ['development', 'test'] in current_app.config['ENV']:
            return {'users': USERS}, 200

        personal_number = hash_to_personal_number(hash_id=hash_id)

        return {
            'type': 'getMyPages',
            'attributes': self.provider.get_mypages(id=personal_number)
        }, 200
