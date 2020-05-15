from marshmallow import Schema, fields, validate, ValidationError, utils, validates, validates_schema
from werkzeug.security import generate_password_hash, check_password_hash
from ..flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity, get_jwt_claims
)
from ..models.users import User


class UserSchema(Schema):

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
    username = fields.Str(required=True,
                          error_messages={"required": "Field is required"},
                          validate=[
                                validate.Length(min=2, max=100,
                                                error=
                                                'Field must be between 2 '
                                                'and 100 characters long')])
    email = fields.Email(required=True,
                         error_messages={"required": "Field is required"},
                         validate=[
                            validate.Length(min=2, max=100,
                                            error=
                                            'Field must be between 2 '
                                            'and 100 characters long')])

    password_hash = fields.Str(required=True,
                               error_messages={"required": "Field is required"},
                               validate=[
                                validate.Length(min=6, max=30,
                                                error=
                                                'Field must be between 6 '
                                                'and 30 characters long')])
    role = fields.Nested(
        'RoleSchema', only=['id'], required=False)

    district = fields.Nested(
        'DistrictSchema', only=['id'], required=False)


class PasswordSchema(Schema):

    id = fields.UUID(required=True,
                     error_messages={
                         "invalid_uuid": "Invalid data for UUID",
                         "required": "Field is required",
                         "null": "Field can not be null"})

    password_change = fields.Str(required=True,
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


class YourPasswordSchema(Schema):

    old_password = fields.Str(required=True,
                              error_messages={"required": "Field is required"},
                              validate=[
                                validate.Length(min=6, max=30,
                                                error=
                                                'Field must be between 6 '
                                                'and 30 characters long')])
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

    @validates_schema
    def validate_password(self, data, **kwargs):
        if data["new_password"] != data["password_confirm"]:
            raise ValidationError(
                {"password_confirm": ["Passwords must match!"]})

    @validates_schema
    def verify_old_password(self, data, **kwargs):
        user = User.query.filter_by(id=get_jwt_claims()['id']).first()
        if not check_password_hash(user.password_hash, data['old_password']):
            raise ValidationError(
                {"old_password": ["Invalid password!"]})