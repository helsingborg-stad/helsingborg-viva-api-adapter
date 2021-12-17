from flask_restful import Resource

from ..libs import Session

from ..libs import authenticate


class TestCookie(Resource):
    method_decorators = [authenticate]

    def get(self):
        session = Session()
        transport = session.get_transport()

        return {
            'transportSessionCookie': str(transport.session.cookies),
        }, 200
