from flask_restful import Resource
from flask import current_app

from app.libs.providers.ekb_abc_provider import EkbABCProvider
from app.libs.classes.session import Session
from app.libs.authenticate_helper import authenticate


class CheckCookie(Resource):
    method_decorators = [authenticate]

    def get(self):
        config = current_app.config['VIVA']

        session = Session(config=config)
        transport = session.get_transport()

        return {
            'transportSessionCookie': str(transport.session.cookies),
        }, 200
