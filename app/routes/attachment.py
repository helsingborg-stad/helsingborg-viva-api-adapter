from flask import jsonify, request
from flask_restful import Resource
from zeep.exceptions import Fault
from marshmallow import ValidationError

from ..libs import VivaMyPages
from ..libs import VivaAttachments

from ..libs import hash_to_personal_number
from ..libs import authenticate


class Attachment(Resource):
    method_decorators = [authenticate]

    def get(self, hash_id=str, attachment_id=str):
        try:
            personal_number = hash_to_personal_number(hash_id=hash_id)

            viva_attachments = VivaAttachments(
                my_pages=VivaMyPages(user=personal_number))

            attachement = viva_attachments.get(attachment_id=attachment_id)

            return attachement

        except Exception as error:
            return {
                'message': f'{error}',
                'code': 400
            }, 400
