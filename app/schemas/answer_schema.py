from marshmallow import Schema, fields


class FieldSchema(Schema):
    id = fields.String(allow_none=True)
    tags = fields.List(fields.Str(required=True), required=True)


class AnswerSchema(Schema):
    field = fields.Nested(FieldSchema(), required=True)
    value = fields.Raw(required=True)
