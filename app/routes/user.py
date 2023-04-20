from typing import Union
from flask_restful import Resource
from flask_apispec.views import MethodResource
from flask_apispec import doc, marshal_with

from marshmallow import Schema, fields as ma_fields

from app.libs.providers.ekb_abc_provider import EkbABCProvider
from app.libs.personal_number_helper import hash_to_personal_number
from app.libs.authenticate_helper import authenticate


class UserResponseSchema(Schema):
    type = ma_fields.String()
    attributes = ma_fields.Nested({
        'personalNumber': ma_fields.String(),
        'firstName': ma_fields.String(),
        'lastName': ma_fields.String(),
        'cases': ma_fields.List(ma_fields.Dict()),
        'persons': ma_fields.List(ma_fields.Dict()),
    })


class User(MethodResource, Resource):
    method_decorators = [authenticate]

    def __init__(self, provider: Union[EkbABCProvider, None] = None) -> None:
        self.provider = provider

    @doc(description='EKB user data', tags=['User'])
    @marshal_with(UserResponseSchema)
    def get(self, hash_id):
        personal_number = hash_to_personal_number(hash_id=hash_id)

        user = self.provider.get_user(
            id=personal_number) if self.provider else None

        return {
            'type': 'EkbUser',
            'attributes': {
                'personalNumber': user.personal_number if user else None,
                'firstName': user.first_name if user else None,
                'lastName': user.last_name if user else None,
                'cases': user.cases if user else None,
                'persons': user.persons if user else None,
            }
        }, 200
