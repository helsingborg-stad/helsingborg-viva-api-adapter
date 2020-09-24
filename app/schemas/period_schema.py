from marshmallow import Schema as SimpleSchema
from marshmallow_jsonapi import fields


class PeriodSchema(SimpleSchema):
    start_date = fields.Date(data_key="startDate")
    end_date = fields.Date(data_key="endDate")
