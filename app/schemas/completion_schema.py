from marshmallow import Schema, fields
from .answer_schema import AnswerSchema


class CompletionSchema(Schema):
    workflow_id = fields.Str(
        data_key='workflowId',
        required=True
    )
    answers = fields.List(
        fields.Nested(AnswerSchema(), required=True),
        required=True
    )
