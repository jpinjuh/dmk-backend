from marshmallow import Schema, fields, validate


class UserSchema(Schema):

    id = fields.UUID(required=True,
                     error_messages={
                         "invalid_uuid": "Invalid data for UUID",
                         "required": "Field is required",
                         "null": "Field can not be null"})

    first_name = fields.Str(required=True,
                      error_messages={"required": "Field is required"},
                      validate=[
                          validate.Length(min=2, max=50,
                                          error=
                                          'Field must be between 2 '
                                          'and 50 characters long')])
    last_name = fields.Str(required=True,
                      error_messages={"required": "Field is required"},
                      validate=[
                          validate.Length(min=2, max=50,
                                          error=
                                          'Field must be between 2 '
                                          'and 50 characters long')])
    username = fields.Str(required=True,
                      error_messages={"required": "Field is required"},
                      validate=[
                          validate.Length(min=2, max=100,
                                          error=
                                          'Field must be between 2 '
                                          'and 100 characters long')])
    email = fields.Str(required=True,
                      error_messages={"required": "Field is required"},
                      validate=[
                          validate.Length(min=2, max=100,
                                          error=
                                          'Field must be between 2 '
                                          'and 100 characters long')])

    password_hash = fields.Str(required=True,
                      error_messages={"required": "Field is required"},
                      validate=[
                          validate.Length(min=6, max=30,
                                          error=
                                          'Field must be between 6 '
                                          'and 30 characters long')])
    role = fields.Nested(
        'RoleSchema', only=['id'], required=False)

    district = fields.Nested(
        'DistrictSchema', only=['id'], required=False)
