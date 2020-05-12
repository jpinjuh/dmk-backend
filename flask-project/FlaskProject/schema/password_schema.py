from marshmallow import Schema, fields, validate, validates_schema, ValidationError, utils
from marshmallow.decorators import (
    POST_DUMP,
    POST_LOAD,
    PRE_DUMP,
    PRE_LOAD,
    VALIDATES,
    VALIDATES_SCHEMA,
)
from marshmallow.utils import (
    RAISE,
    EXCLUDE,
    INCLUDE,
    missing,
    set_value,
    get_value,
    is_collection,
    is_instance_or_subclass,
    is_iterable_but_not_string,
)


class PasswordSchema(Schema):

    new_password = fields.Str(required=True,
                      error_messages={"required": "Field is required"},
                      validate=[
                          validate.Length(min=6, max=30,
                                          error=
                                          'Field must be between 6 '
                                          'and 30 characters long')])

    password_confirm = fields.Str(required=True,
                      error_messages={"required": "Field is required"},
                      validate=[
                          validate.Length(min=6, max=30,
                                          error=
                                          'Field must be between 6 '
                                          'and 30 characters long')])
                          #validate.Equal(new_password)])

    @validates_schema
    def validate_password(self, data, **kwargs):
        if data["new_password"] != data["password_confirm"]:
            raise ValidationError('Passwords must match!')



