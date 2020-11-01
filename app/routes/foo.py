from flask import jsonify, request
from flask_restful import Resource
from marshmallow import ValidationError

from ..libs import parse_application
from ..schemas import ApplicationSchema


class Foo(Resource):
    def post(self):
        json_payload = request.json

        application_schema = ApplicationSchema()

        try:
            validated_data = application_schema.load(json_payload)
        except ValidationError as error:
            return jsonify(error.messages)

        parsed_data = parse_application(
            answers=validated_data['answers'],
            period=validated_data['period']
        )

        if not parsed_data:
            return {
                'error': 'No data'
            }, 400

        return parsed_data, 200
