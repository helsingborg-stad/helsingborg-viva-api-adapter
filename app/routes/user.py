from typing import Union
from flask_restful import Resource
from flask_apispec.views import MethodResource
from flask_apispec import doc, marshal_with

from marshmallow import Schema, fields as ma_fields

from app.libs.providers.ekb_abc_provider import EkbABCProvider
from app.libs.personal_number_helper import hash_to_personal_number
from app.libs.authenticate_helper import authenticate


class GetEkbUserSchema(Schema):
    type = ma_fields.String()
    attributes = ma_fields.Nested({
        'personalNumber': ma_fields.String(attribute='personalNumber'),
    })


class User(MethodResource, Resource):
    method_decorators = [authenticate]

    def __init__(self, provider: Union[EkbABCProvider, None] = None) -> None:
        self.provider = provider

    @doc(description='EKB user data', tags=['User'],)
    @marshal_with(GetEkbUserSchema)
    def get(self, hash_id) -> tuple:
        personal_number = hash_to_personal_number(hash_id=hash_id)

        return {
            'type': 'EkbUser',
            'attributes': {
                'personalNumber': personal_number,
            }
        }, 200
