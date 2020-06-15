from marshmallow import Schema, fields, validate


class ChrismNoteSchema(Schema):

    id = fields.UUID(required=True,
                     error_messages={
                         "invalid_uuid": "Invalid data for UUID",
                         "required": "Field is required",
                         "null": "Field can not be null"})

    person = fields.Nested(
        'PersonSchema', only=['id'], required=True)

    best_man = fields.Nested(
        'PersonSchema', only=['id'], required=True)
