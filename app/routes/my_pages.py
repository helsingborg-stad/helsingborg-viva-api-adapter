from flask import current_app
from flask_restful import Resource, reqparse
import re

from .. import data
from ..libs.my_pages import MyPages as VivaMyPages


class MyPages(Resource):
    def get(self, hash_id=None):
        if not hash_id:
            return {
                'users': data.USERS,
            }

        return {
            'user': {
                'pnr': self._parse_pnr(hash_id),
                **data.USERS[hash_id]
            }
        }, 200

    @classmethod
    def _parse_pnr(self, number=int):
        decoded = str(data.hashids.decode(number)[0])
        regex = re.compile('([0-9]{6})([0-9]{4})')
        parts = regex.match(decoded).groups()
        formated = 'T'.join(parts)
        return formated
