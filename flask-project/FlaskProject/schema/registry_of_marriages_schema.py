from marshmallow import Schema, fields, validate


class RegistryOfMarriagesSchema(Schema):

    id = fields.UUID(required=True,
                     error_messages={
                         "invalid_uuid": "Invalid data for UUID",
                         "required": "Field is required",
                         "null": "Field can not be null"})

    person_id = fields.Nested(
        'PersonSchema', only=['id'], required=True)

    person2_id = fields.Nested(
        'PersonSchema', only=['id'], required=True)

    best_man = fields.Nested(
        'PersonSchema', only=['id'], required=True)

    best_man2 = fields.Nested(
        'PersonSchema', only=['id'], required=True)



