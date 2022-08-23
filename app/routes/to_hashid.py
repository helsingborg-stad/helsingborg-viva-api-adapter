from flask_restful import Resource

from app.libs.personal_number_helper import get_hash_ids
from app.libs.authenticate_helper import authenticate


class ToHashId(Resource):
    method_decorators = [authenticate]

    def get(self, personal_number: int):

        hashid = get_hash_ids().encode(personal_number)

        response = {
            'hashid': hashid
        }

        return response, 200
