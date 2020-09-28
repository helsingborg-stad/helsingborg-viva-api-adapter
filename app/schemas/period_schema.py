from marshmallow import Schema as SimpleSchema
from marshmallow_jsonapi import fields


class PeriodSchema(SimpleSchema):
    start_date = fields.String(data_key='startDate')
    end_date = fields.String(data_key='endDate')
