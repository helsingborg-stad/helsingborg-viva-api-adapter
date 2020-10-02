from marshmallow import Schema as SimpleSchema
from marshmallow_jsonapi import fields


class ResponseSchema(SimpleSchema):
    errorCode = fields.String(data_key='ERRORCODE')
    errorMessage = fields.String(data_key='ERRORMESSAGE')
    status = fields.String(data_key='STATUS')
    idenclair = fields.String(data_key='IDENCLAIR', allow_none=True)
    id = fields.String(data_key='ID', allow_none=True)
