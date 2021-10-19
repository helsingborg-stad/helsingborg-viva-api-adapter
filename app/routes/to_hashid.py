from flask_restful import Resource
from ..libs import hashids_instance
from ..libs import authenticate


class ToHashId(Resource):
    method_decorators = [authenticate]

    def get(self, personal_number: int):

        hashid = hashids_instance.encode(personal_number)

        response = {
            'hashid': hashid
        }

        return response, 200
