from marshmallow import Schema as SimpleSchema, fields


class ResponseSchema(SimpleSchema):
    errorCode = fields.String(data_key='ERRORCODE', allow_none=True)
    errorMessage = fields.String(data_key='ERRORMESSAGE', allow_none=True)
    status = fields.String(data_key='STATUS', allow_none=True)
    idenclair = fields.String(data_key='IDENCLAIR', allow_none=True)
    id = fields.String(data_key='ID', allow_none=True)
