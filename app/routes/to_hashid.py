from flask_restful import Resource
from ..libs import get_hash_ids
from ..libs import authenticate


class ToHashId(Resource):
    method_decorators = [authenticate]

    def get(self, personal_number: int):

        hashid = get_hash_ids().encode(personal_number)

        response = {
            'hashid': hashid
        }

        return response, 200
