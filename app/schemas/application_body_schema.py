from marshmallow import validate, Schema, fields


class ApplicationBodySchema(Schema):
    expenses = fields.Raw(required=True)
    incomes = fields.Raw(required=True)
    housingInfo = fields.Raw(required=True)
    personalInfo = fields.Raw(required=True)
    receivingBenefits = fields.String(required=False, allow_none=True)
