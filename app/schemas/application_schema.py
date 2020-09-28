from marshmallow import validate, Schema, fields
from .period_schema import PeriodSchema


class ApplicationBodySchema(Schema):
    expenses = fields.Raw(required=True)
    incomes = fields.Raw(required=True)
    housingInfo = fields.Raw(required=True)
    personalInfo = fields.Raw(required=True)
    receivingBenefits = fields.String(required=False, allow_none=True)


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
    application_body = fields.Nested(ApplicationBodySchema(), data_key='applicationBody', required=True)
