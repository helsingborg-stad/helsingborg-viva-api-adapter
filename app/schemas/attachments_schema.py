import base64
from marshmallow import Schema, fields, validates, ValidationError


class AttachmentsSchema(Schema):
    hashid = fields.Str(required=True)
    id = fields.Str(
        data_key='attachmentId',
        required=True
    )
    name = fields.Str(
        data_key='filename',
        required=True
    )
    file_base64 = fields.Str(
        data_key='fileBase64',
        required=True
    )

    @validates('file_base64')
    def validate_file(self, file_base64):
        if isinstance(file_base64, str):
            file_bytes = bytes(file_base64, 'ascii')
        elif isinstance(file_base64, bytes):
            file_bytes = file_base64
        else:
            raise ValidationError('Value must be string or bytes')

        return base64.b64encode(base64.b64decode(file_base64)) == file_base64
