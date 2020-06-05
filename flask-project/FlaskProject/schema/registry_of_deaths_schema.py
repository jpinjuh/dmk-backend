from marshmallow import Schema, fields, validate


class RegistryOfDeathsSchema(Schema):

    id = fields.UUID(required=True,
                     error_messages={
                         "invalid_uuid": "Invalid data for UUID",
                         "required": "Field is required",
                         "null": "Field can not be null"})

    person_id = fields.Nested(
        'PersonSchema', only=['id'], required=False)

    date_of_death = fields.Date(required=True,
                                error_messages={"required": "Field is required"})

    place_of_death = fields.Nested(
        'CitySchema', only=['id'], required=True)

    place_of_burial = fields.Nested(
        'ListItemSchema', only=['id'], required=True)