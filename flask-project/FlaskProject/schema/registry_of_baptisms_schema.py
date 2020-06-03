from marshmallow import Schema, fields, validate


class RegistryOfBaptismsSchema(Schema):

    id = fields.UUID(required=True,
                     error_messages={
                         "invalid_uuid": "Invalid data for UUID",
                         "required": "Field is required",
                         "null": "Field can not be null"})

    name = fields.Str(required=True,
                      error_messages={"required": "Field is required"},
                      validate=[
                          validate.Length(min=2, max=50,
                                          error=
                                          'Field must be between 2 '
                                          'and 50 characters long')])
    surname = fields.Str(required=True,
                         error_messages={"required": "Field is required"},
                         validate=[
                           validate.Length(min=2, max=50,
                                           error=
                                           'Field must be between 2 '
                                           'and 50 characters long')])
    birth_date = fields.Date(required=True,
                             error_messages={"required": "Field is required"})

    identity_number = fields.Str(required=True,
                         error_messages={"required": "Field is required"},
                         validate=[
                           validate.Length(min=13, max=20,
                                           error=
                                           'Field must be between 13 '
                                           'and 20 characters long')])
    person = fields.Nested(
        'PersonSchema', only=['id'], required=False)

    best_man = fields.Nested(
        'PersonSchema', only=['id'], required=True)

    birth_place = fields.Nested(
        'CitySchema', only=['id'], required=True)

    child = fields.Nested(
        'ListItemSchema', only=['id'], required=True)

    parents_canonically_married = fields.Nested(
        'ListItemSchema', only=['id'], required=True)