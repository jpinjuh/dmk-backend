from marshmallow import Schema, fields, validate


class PersonExtraInfoSchema(Schema):

    id = fields.UUID(required=True,
                     error_messages={
                         "invalid_uuid": "Invalid data for UUID",
                         "required": "Field is required",
                         "null": "Field can not be null"})

    person_id = fields.Nested(
        'PersonSchema', only=['id'], required=True)

    baptism_district = fields.Nested(
        'DistrictSchema', only=['id'], required=True)

    baptism_date = fields.Date(required=True,
                               error_messages={"required": "Field is required"})

    parents_canonically_married = fields.Nested(
        'ListItemSchema', only=['id'], required=True)
