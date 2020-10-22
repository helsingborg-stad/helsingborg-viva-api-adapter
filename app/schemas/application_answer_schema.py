from marshmallow import validate, Schema, fields


class ApplicationAnswerSchema(Schema):
    field = fields.Dict(
        field_id=fields.Str(data_key='id'),
        tags=fields.List(fields.Str()), required=True)
    field_id = fields.Str(data_key='id')
    field_type = fields.Str(data_key='type')
    value = fields.Raw()
