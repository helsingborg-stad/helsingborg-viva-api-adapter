from flask_restful import Resource


class Index(Resource):
    def get(self):
        return {
            'message': 'Welcome to the Viva ADApter (VADA) api',
        }, 200
