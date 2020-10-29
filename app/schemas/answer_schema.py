from marshmallow import validate, Schema, fields


class AnswerSchema(Schema):
    field = fields.Dict(
        tags=fields.List(fields.Str()),
        required=True
    )
    field_type = fields.Str(data_key='type')
    value = fields.Raw()
