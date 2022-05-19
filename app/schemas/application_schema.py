from marshmallow import validate, Schema, fields

from .answer_schema import AnswerSchema
from .completion_schema import AttachmentSchema


class ApplicationSchema(Schema):
    application_type = fields.Str(
        data_key='applicationType',
        required=True,
        validate=validate.OneOf(['recurrent', 'new'])
    )
    hashid = fields.Str(required=True)
    workflow_id = fields.Str(
        data_key='workflowId',
        required=True
    )
    answers = fields.List(
        fields.Nested(AnswerSchema(), required=True),
        required=True
    )
    attachments = fields.List(
        fields.Nested(AttachmentSchema(), required=True),
        required=False
    )
    raw_data = fields.Raw(
        data_key='rawData',
        required=True
    )
    raw_data_type = fields.Str(
        data_key='rawDataType',
        required=True,
        validate=validate.OneOf(['pdf'])
    )
