from flask import jsonify, request
from flask_restful import Resource, abort, wraps
from marshmallow import ValidationError

from ..libs import parse_application
from ..schemas import ApplicationSchema


def authentication():
    return True

def authenticate(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if not getattr(f, 'authenticate', True):
            return f(*args, **kwargs)

        acct = authentication()
        if acct:
            return f(*args, **kwargs)

        abort(http_status_code=401)

    return wrapper


class Foo(Resource):
    method_decorators = [authenticate]

    def post(self, *args, **kwargs):
        json_payload = request.json

        application_schema = ApplicationSchema()

        try:
            validated_data = application_schema.load(json_payload)
        except ValidationError as error:
            return jsonify(error.messages)

        parsed_application = parse_application(
            answers=validated_data['answers'],
            period=validated_data['period']
        )

        if not parsed_application:
            return {
                'error': 'No data'
            }, 400

        return parsed_application, 200
