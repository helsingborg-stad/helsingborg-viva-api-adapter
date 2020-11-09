from marshmallow import validate, Schema, fields


class FieldSchema(Schema):
    tags = fields.List(fields.Str(required=True), required=True)


class AnswerSchema(Schema):
    field = fields.Nested(FieldSchema(), required=True)
    value = fields.Integer(required=True)
