from marshmallow import Schema, fields, validate


class PrivilegeSchema(Schema):

    id = fields.UUID(required=True,
                     error_messages={
                         "invalid_uuid": "Invalid data for UUID",
                         "required": "Field is required",
                         "null": "Field can not be null"})

    role = fields.Nested(
        'RoleSchema', only=['id'], required=True)

    permission = fields.Nested(
        'PermissionSchema', only=['id'], required=True)
