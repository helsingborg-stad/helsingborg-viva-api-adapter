from marshmallow import Schema, fields


class PeriodSchema(Schema):
    start_date = fields.Str(data_key='startDate', required=True)
    end_date = fields.Str(data_key='endDate', required=True)
