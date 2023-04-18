from flask_restful import Resource

from app.libs.providers.ekb_abc_provider import EkbABCProvider
from app.libs.personal_number_helper import hash_to_personal_number
from app.libs.authenticate_helper import authenticate


class User(Resource):
    method_decorators = [authenticate]

    def __init__(self, provider: EkbABCProvider) -> None:
        self.provider = provider

    def get(self, hash_id) -> tuple:
        personal_number = hash_to_personal_number(hash_id=hash_id)

        return {
            'type': 'EkbUser',
            'attributes': {
                'personalNumber': personal_number,
            }
        }, 200
