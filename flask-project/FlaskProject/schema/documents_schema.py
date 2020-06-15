from marshmallow import Schema, fields, validate


class DocumentSchema(Schema):

    id = fields.UUID(required=True,
                     error_messages={
                         "invalid_uuid": "Invalid data for UUID",
                         "required": "Field is required",
                         "null": "Field can not be null"})

    act_date = fields.Date(required=True,
                           error_messages={"required": "Field is required"})

    document_number = fields.Str(required=True,
                      error_messages={"required": "Field is required"},
                      validate=[
                          validate.Length(min=2, max=30,
                                          error=
                                          'Field must be between 2 '
                                          'and 30 characters long')])
    volume = fields.Str(required=False, validate=[
                          validate.Length(min=1, max=10,
                                          error=
                                          'Field must be between 1 '
                                          'and 10 characters long')])
    year = fields.Integer(required=False)
    page = fields.Integer(required=False)
    number = fields.Integer(required=False)

    document_type = fields.Nested(
        'ListItemSchema', only=['id'], required=False)

    person = fields.Nested(
        'PersonSchema', only=['id'], required=True)

    person2 = fields.Nested(
        'PersonSchema', only=['id'], required=False)

    act_performed = fields.Nested(
        'UserSchema', only=['id'], required=True)

    district = fields.Nested(
        'DistrictSchema', only=['id'], required=True)

    user_created = fields.Nested(
        'UserSchema', only=['id'], required=False)