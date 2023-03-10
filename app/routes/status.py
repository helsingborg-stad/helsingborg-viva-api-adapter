from flask_restful import Resource

from app.libs.personal_number_helper import hash_to_personal_number
from app.libs.data_domain.ekb_provider import EkbProvider
from app.libs.authenticate_helper import authenticate


class Status(Resource):
    method_decorators = [authenticate]

    def __init__(self, ekb: EkbProvider):
        self.ekb = ekb

    def get(self, hash_id):
        personal_number = hash_to_personal_number(hash_id=hash_id)

        status = self.ekb.get_status(personal_number)
        response = {
            'type': 'getApplicationsStatus',
            'attributes': {
                'status': status.get_status_text()
            }
        }

        return response, 200
