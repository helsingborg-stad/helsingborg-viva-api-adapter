from marshmallow import validate, Schema, fields


class AttachmentSchema(Schema):
    id = fields.String(required=True)
    name = fields.String(required=True)
    category = fields.String(
        required=True,
        validate=validate.OneOf(['incomes', 'expenses', 'completion'])
    )
    file_base64 = fields.String(
        data_key='fileBase64',
        required=True
    )


class CompletionSchema(Schema):
    workflow_id = fields.String(
        data_key='workflowId',
        required=True
    )
    attachments = fields.List(
        fields.Nested(AttachmentSchema(), required=True),
        required=True
    )
