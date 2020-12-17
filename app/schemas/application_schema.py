from marshmallow import validate, Schema, fields
from .answer_schema import AnswerSchema


class ApplicationSchema(Schema):
    application_type = fields.Str(
        data_key='applicationType',
        required=True,
        validate=validate.OneOf(['recurrent', 'basic'])
    )
    hashid = fields.Str(required=True)
    answers = fields.List(
        fields.Nested(AnswerSchema(), required=True),
        required=True
    )
