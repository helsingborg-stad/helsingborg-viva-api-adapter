from marshmallow import validate, Schema, fields
from .period_schema import PeriodSchema
from .answer_schema import AnswerSchema


class ApplicationSchema(Schema):
    application_type = fields.Str(
        data_key='applicationType',
        required=True,
        validate=validate.OneOf(['recurrent', 'basic']),
    )
    client_ip = fields.Str(data_key='clientIp', required=True)
    workflow_id = fields.Str(data_key='workflowId', required=True)
    applicant = fields.Str(required=True)
    period = fields.Nested(PeriodSchema(), required=True)
    answers = fields.List(
        fields.Nested(AnswerSchema(), required=True),
        required=True
    )
