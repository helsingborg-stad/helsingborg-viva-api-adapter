from flask import current_app
from flask_restful import Resource

from ..libs.session import Session


class TestCookie(Resource):
    def get(self):
        sess = Session()
        trans = sess.get_transport()

        return {
            'SessionCookie': str(Session._cookie),
            'transportSessionCookie': str(trans.session.cookies),
        }, 200
