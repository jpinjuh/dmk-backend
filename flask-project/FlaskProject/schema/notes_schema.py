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

    chrism_date = fields.Date(required=False)

    marriage_district = fields.Nested(
        'DistrictSchema', only=['id'], required=False)

    marriage_date = fields.Date(required=False)

    spouse_name = fields.Str(required=False)

    other_notes = fields.Str(required=False)

