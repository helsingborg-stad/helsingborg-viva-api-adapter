from marshmallow import Schema, fields


class PeriodSchema(Schema):
    start_date = fields.Number(data_key='startDate', required=True)
    end_date = fields.Number(data_key='endDate', required=True)
