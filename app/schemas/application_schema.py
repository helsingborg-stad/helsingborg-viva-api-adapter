from marshmallow import validate, Schema, fields
from .period_schema import PeriodSchema


class ApplicationDataSchema(Schema):
    expenses = fields.Raw(required=True)
    incomes = fields.Raw(required=True)
    housingInfo = fields.Raw(required=True)
    personalInfo = fields.Raw(required=True)
    receivingBenefits = fields.String(required=False)


class ApplicationSchema(Schema):
    application_type = fields.Str(validate=validate.OneOf(
        ["recurrent", "basic"]), required=True, data_key="applicationType")
    period = fields.Nested(PeriodSchema())
    personal_number = fields.Str(data_key="personalNumber", required=True)
    client_ip = fields.Str(data_key="clientIp", required=True)
    workflow_id = fields.Str(data_key="workflowId", required=True)
    data = fields.Nested(ApplicationDataSchema(), required=True)
