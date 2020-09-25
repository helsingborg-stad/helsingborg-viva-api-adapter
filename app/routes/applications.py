from flask import jsonify, request
from marshmallow import ValidationError
from flask_restful import Resource

from ..libs.viva_application import VivaApplication
from ..libs import decode_hash_personal_number
from ..schemas.application_schema import ApplicationSchema

cost_types = ['EXPENSES', "INCOMES"]


def parse_application_data(data, period, parent_key=None, initial_data={}):
    for key, value in data.items():
        if parent_key == None and type(value) is dict and key.upper() in cost_types:
            # create a new key on the initial_data param and call this function again to create the value for the key.
            key = key.upper()  # transform the key to uppercase to match zeep viva json object
            initial_data[key] = parse_application_data(
                value, period, parent_key=key, initial_data=[])

        if parent_key in cost_types and type(value) is dict:
            # create a single income or expense and add it to the array passed thorugh initial_data.
            applies_to = "coapplication" if "Partner" in key else "applicant"
            period_string = f"{period['start_date']} - {period['end_date']}"

            initial_data.append({parent_key[:-1]: {
                "TYPE": key,
                "APPLIESTO": applies_to,
                "FREQUENCY": 12,
                "AMOUNT": value['amount'],
                "PERIOD": period_string,
                "DATE": value['date']
            }})
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

        # this object is missing the root key "‹"
        initial_data = {
            "RAWDATATYPE": "PDF",
            "HOUSEHOLDINFO": "",
        }

        viva_application_data = parse_application_data(
            data=validated_data['data'], period=validated_data['period'], initial_data=initial_data)
        print(viva_application_data)
        # pass viva_application_data to viva and
        # application = VivaApplication(
        #     application_type=validated_data['application_type'],
        #     personal_number=parse_hash(
        #         hashid=validated_data['personal_number']),
        #     client_ip=validated_data['client_ip'],
        #     workflow_id=validated_data['workflow_id'],
        #     application_data=viva_application_data
        # )ß

        # return something better as an response
        return jsonify(viva_application_data)


# application = VivaApplication(
#     application_type=json_payload.application_type,
#     user=parse_hash(hashid=json_payload.user_hash),
#     application_data=json_payload.data
# )

        application = VivaApplication(
            application_type=json_payload.application_type,
            user=decode_hash_personal_number(hash_id=json_payload.user_hash),
            application_data=json_payload.data
        )

# return jsonify({"ok": "success"})

# {
#     "application_type": "renew",
#     "user_hash": "INSERT_HASHED_PERSON_NUMBER_HERE ie: <197105016161>",
#     "data": {
#         "ç": {
#             "RAWDATA": "TESTING CREATE RE-APPLICATION USING VADA API ADAPTER",
#             "RAWDATATYPE": "PDF",
#             "HOUSEHOLDINFO": "STUFF",
#             "EXPENSES": [
#                 {
#                  "EXPENSE": {
#                      "TYPE": "Mobiltelefon",
#                      "DESCRIPTION": "avtal",
#                      "APPLIESTO": "coapplicant",
#                      "FREQUENCY": 12,
#                      "PERIOD": "2020-05-01 - 2020-05-31",
#                      "AMOUNT": 199,
#                      "DATE": "2020-05-08"
#                  }
#                 },
#                 {
#                     "EXPENSE": {
#                         "TYPE": "Mobiltelefon",
#                         "DESCRIPTION": "avtal",
#                         "APPLIESTO": "applicant",
#                         "FREQUENCY": 12,
#                         "PERIOD": "2020-05-01 - 2020-05-31",
#                         "AMOUNT": 169,
#                         "DATE": "2020-05-08"
#                     }
#                 }
#             ],
#             "INCOMES": [
#                 {
#                     "INCOME": {
#                         "TYPE": "Hyra",
#                         "DESCRIPTION": "Uthyrning av garage",
#                         "APPLIESTO": "applicant",
#                         "FREQUENCY": 12,
#                         "PERIOD": "2020-05-01 - 2020-05-31",
#                         "AMOUNT": 250,
#                         "DATE": "2020-05-08"
#                     }
#                 }
#             ],
#             "ASSETS": [
#                 {
#                     "ASSET": {
#                         "TYPE": "MC",
#                         "DESCRIPTION": "Motocross",
#                         "APPLIESTO": "applicant",
#                         "AMOUNT": 16000
#                     }
#                 },
#                 {
#                     "ASSET": {
#                         "TYPE": "Bil",
#                         "DESCRIPTION": "Opel Ascona med körförbud",
#                         "APPLIESTO": "applicant",
#                         "AMOUNT": 4000
#                     }
#                 }
#             ],
#             "OTHER": "Lite text från Övriga upplysningar. Till exempel om du sökt utbildning eller planering med Arbetsförmedlingen.",
#             "SIGNATURES": [
#                 {
#                     "SIGNATURE": {
#                      "ID": "19710501T6161",
#                      "VISIBLEDATA": "Härmed intygar jag att...",
#                      "NONVISIBLEDATA": "data",
#                      "SIGNATUREDATA": "data",
#                      "OCSPRESPONSE": "data",
#                      "TRANSACTIONID": 1232,
#                      "IP": "127.0.0.1",
#                      "TIMESTAMP": "2020-05-08T23:46:00+01:00"
#                     }
#                 }
#             ]
#         },
#         "NOTIFYINFOS": [
#             {
#                 "NOTIFYINFO": {
#                     "ID": "19710501T6161",
#                     "ADDRESS": "070555555",
#                     "ADDRESSTYPE": "sms"
#                 }
#             }
#         ]
#     }
# }
