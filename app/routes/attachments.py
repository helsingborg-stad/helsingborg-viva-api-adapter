from flask import jsonify, request
from flask_restful import Resource
from zeep.exceptions import Fault
from marshmallow import ValidationError

from ..libs import VivaMyPages
from ..libs import VivaAttachments

from ..libs import hash_to_personal_number
from ..libs import authenticate

from ..schemas import AttachmentsSchema


class Attachments(Resource):
    method_decorators = [authenticate]

    def get(self, hash_id=str, attachment_id=str):
        try:
            personal_number = hash_to_personal_number(hash_id=hash_id)

            viva_attachments = VivaAttachments(
                my_pages=VivaMyPages(user=personal_number))

            get_result = viva_attachments.get(attachment_id=attachment_id)

            return get_result

        except Exception as error:
            return {
                'message': f'{error}',
                'code': 400
            }, 400

    def post(self):
        try:
            json_payload = request.json

            attachments_schema = AttachmentsSchema()
            validated_attachment = attachments_schema.load(json_payload)

            personal_number = hash_to_personal_number(
                hash_id=validated_attachment['hashid'])

            viva_attachments = VivaAttachments(
                my_pages=VivaMyPages(user=personal_number))

            save_result = viva_attachments.save(
                attachment=validated_attachment)

            return save_result

        except Exception as error:
            return {
                'message': f'{error}',
                'code': 400
            }, 400
