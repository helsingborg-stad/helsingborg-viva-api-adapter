from flask_restful import Resource

from .. import data


class MyPagesList(Resource):
    def get(self):
        return {
            'users': data.USERS
        }, 200
