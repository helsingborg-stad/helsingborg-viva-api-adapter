from flask_restful import Resource

from app.libs.classes.session import Session
from app.libs.authenticate_helper import authenticate


class CheckCookie(Resource):
    method_decorators = [authenticate]

    def get(self):
        session = Session(config={'cookie_auth_name': 'DomAuthSessId'})
        transport = session.get_transport()

        return {
            'transportSessionCookie': str(transport.session.cookies),
        }, 200
