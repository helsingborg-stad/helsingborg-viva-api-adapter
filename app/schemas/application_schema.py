from marshmallow import validate, Schema, fields
from . import PeriodSchema
from . import ApplicationBodySchema


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
    application_body = fields.Nested(
        ApplicationBodySchema(), data_key='applicationBody', required=True)
