from marshmallow import Schema, fields, validate


class ListItemSchema(Schema):

    id = fields.UUID(required=True,
                     error_messages={
                         "invalid_uuid": "Invalid data for UUID",
                         "required": "Field is required",
                         "null": "Field can not be null"})

    value = fields.Str(required=True,
                      error_messages={"required": "Field is required"},
                      validate=[
                          validate.Length(min=1, max=100,
                                          error=
                                          'Field must be between 1 '
                                          'and 100 characters long')])

    description = fields.Str()

    list = fields.Nested(
        'ListSchema', only=['id'], required=True)
