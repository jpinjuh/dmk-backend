from marshmallow import Schema, fields, validate


class PersonsHistorySchema(Schema):

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
    maiden_name = fields.Str(validate=[
                          validate.Length(min=2, max=50,
                                          error=
                                          'Field must be between 2 '
                                          'and 50 characters long')])
    birth_date = fields.Date(required=True,
                             error_messages={"required": "Field is required"})

    birth_place = fields.Nested(
        'CitySchema', only=['id'], required=True)

    identity_number = fields.Str(validate=[
                          validate.Length(min=13, max=20,
                                          error=
                                          'Field must be between 13'
                                          'and 20 characters long')])
    father = fields.Nested(
        'PersonSchema', only=['id'], required=True)

    mother = fields.Nested(
        'PersonSchema', only=['id'], required=False)

    district = fields.Nested(
        'DistrictSchema', only=['id'], required=True)

    religion = fields.Nested(
        'ListItemSchema', only=['id'], required=True)

    person = fields.Nested(
        'PersonSchema', only=['id'], required=True)

    user_created = fields.Nested(
        'UserSchema', only=['id'], required=True)