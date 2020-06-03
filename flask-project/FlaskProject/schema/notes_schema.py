from marshmallow import Schema, fields, validate


class NoteSchema(Schema):

    id = fields.UUID(required=True,
                     error_messages={
                         "invalid_uuid": "Invalid data for UUID",
                         "required": "Field is required",
                         "null": "Field can not be null"})

    person_id = fields.Nested(
        'PersonSchema', only=['id'], required=False)

    chrism_place = fields.Nested(
        'CitySchema', only=['id'], required=False)

    chrism_date = fields.Date(required=True,
                              error_messages={"required": "Field is required"})

    marriage_district = fields.Nested(
        'DistrictSchema', only=['id'], required=False)

    marriage_date = fields.Date(required=True,
                                error_messages={"required": "Field is required"})

    spouse_name = fields.Str(required=True,
                             error_messages={"required": "Field is required"},
                             validate=[
                              validate.Length(min=2, max=50,
                                              error=
                                              'Field must be between 2 '
                                              'and 50 characters long')])
    other_notes = fields.Str(required=True,
                             error_messages={"required": "Field is required"},
                             validate=[
                              validate.Length(min=2, max=50,
                                              error=
                                              'Field must be between 2 '
                                              'and 50 characters long')])

