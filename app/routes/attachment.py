from flask_restful import Resource

from app.libs.classes.viva_my_pages import VivaMyPages
from app.libs.classes.viva_attachments import VivaAttachments

from app.libs.personal_number_helper import hash_to_personal_number
from app.libs.authenticate_helper import authenticate


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
