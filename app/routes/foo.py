from flask import jsonify, request
from flask_restful import Resource
from marshmallow import ValidationError

from ..libs import parse_application, authenticate
from ..schemas import ApplicationSchema


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
