from flask_restful import Resource, fields, marshal_with

from app.libs.providers.ekb_abc_provider import EkbABCProvider
from app.libs.personal_number_helper import hash_to_personal_number
from app.libs.authenticate_helper import authenticate


get_user_response_schema = {
    'type': fields.String,
    'attributes': fields.Nested({
        'personalNumber': fields.String(attribute='personalNumber'),
    })
}


class User(Resource):
    method_decorators = [authenticate]

    def __init__(self, provider: EkbABCProvider) -> None:
        self.provider = provider

    @ marshal_with(get_user_response_schema)
    def get(self, hash_id) -> tuple:
        '''
        Get user by hash_id
        '''

        personal_number = hash_to_personal_number(hash_id=hash_id)

        return {
            'type': 'EkbUser',
            'attributes': {
                'personalNumber': personal_number,
            }
        }, 200
