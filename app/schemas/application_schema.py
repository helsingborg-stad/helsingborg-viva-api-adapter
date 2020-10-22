from marshmallow import validate, Schema, fields
from .period_schema import PeriodSchema
from .application_answer_schema import ApplicationAnswerSchema


class ApplicationSchema(Schema):
    application_type = fields.Str(
        data_key='applicationType',
        required=True,
        validate=validate.OneOf(['recurrent', 'basic']),
    )
    client_ip = fields.Str(data_key='clientIp', required=True)
    workflow_id = fields.Str(data_key='workflowId', required=True)
    personal_number = fields.Str(data_key='personalNumber', required=True)
    period = fields.Nested(PeriodSchema())
    answers = fields.List(
        fields.Nested(ApplicationAnswerSchema()), required=True
    )
