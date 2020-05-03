from flask import current_app
from flask_restful import Resource, reqparse
from hashids import Hashids

from .. import data

hashids = Hashids(
    salt=current_app.config['SALT'],
    min_length=32
)


class MyPages(Resource):
    def get(self, hash_id):
        if hash_id is None:
            return 'Not found', 404

        pnr_decoded = hashids.decode(hash_id)[0]

        return {
            'users': data.USERS,
            'user': {
                'pnr': pnr_decoded,
                **data.USERS[hash_id]
            }
        }, 200
