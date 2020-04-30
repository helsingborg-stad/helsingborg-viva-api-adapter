from flask_restful import Resource, reqparse


class Applications(Resource):
    def get(self, pnr):
        if pnr is None:
            return 'Not found', 404
        else:
            return 'APPLICATIONS LIST'
