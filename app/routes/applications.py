from flask import jsonify, request
from marshmallow import ValidationError
from flask_restful import Resource

from ..libs.viva_application import VivaApplication
from ..libs import decode_hash_personal_number
from ..schemas.application_schema import ApplicationSchema


cost_types = ['EXPENSES', 'INCOMES']


def parse_application_data(data, period, parent_key=None, initial_data=dict):
    for key, value in data.items():
        if parent_key == None and type(value) is dict and key.upper() in cost_types:
            # create a new key on the initial_data param and call this function again to create the value for the key.
            key = key.upper()  # transform the key to uppercase to match zeep viva json object
            initial_data[key] = parse_application_data(
                value, period, parent_key=key, initial_data=[]
            )

        if parent_key in cost_types and type(value) is dict:
            # create a single income or expense and add it to the array passed thorugh initial_data.
            applies_to = 'coapplication' if 'Partner' in key else 'applicant'
            period_string = f'{period["start_date"]} - {period["end_date"]}'

            initial_data.append(
                {
                    parent_key[:-1]: {
                        'TYPE': key,
                        'APPLIESTO': applies_to,
                        'PERIOD': period_string,
                        'FREQUENCY': 12,
                        'AMOUNT': value['amount'],
                        'DATE': value['date'],
                        'DESCRIPTION': '',
                    }
                }
            )

    return initial_data


class Applications(Resource):
    def get(self):
        return 'APPLICATIONS LIST'

    def post(self):
        json_payload = request.json
        schema = ApplicationSchema()

        try:
            validated_data = schema.load(json_payload)
        except ValidationError as error:
            return jsonify(error.messages)

        viva_application_data = parse_application_data(
            data=validated_data['application_body'],
            period=validated_data['period'],
            initial_data={
                'RAWDATA': '',
                'RAWDATATYPE': 'PDF',
                'HOUSEHOLDINFO': '',
                'OTHER': ''
            }
        )

        application = VivaApplication(
            application_type=validated_data['application_type'],
            application_data=viva_application_data,
            personal_number=parse_hash(
                hashid=validated_data['personal_number']),
            client_ip=validated_data['client_ip'],
            workflow_id=validated_data['workflow_id'],
            period=validated_data['period'],
        )

        response = application.create()

        return response
        # return jsonify({"ok": "success"})
