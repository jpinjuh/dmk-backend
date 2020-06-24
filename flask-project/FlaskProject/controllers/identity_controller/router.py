from flask import request, jsonify
from ...flask_jwt_extended import (
    jwt_required, create_access_token,
    get_jwt_identity, get_jwt_claims
)
from ...controllers.users_controller.controller import UserController
from ... import bpp, User
from ...general import Status
from ...general.route_decorators import allow_access
from ...schema import YourPasswordSchema
from werkzeug.security import generate_password_hash
import datetime


@bpp.route('/login', methods=('POST',))
def login():
    data = request.get_json()
    user = User.authenticate(**data)

    if not user:
        return jsonify(
            message='Invalid credentials',
            status=Status.status_unsuccessfully_processed().__dict__)
    payload = {
        'id': user.id.__str__(),
        'first_name': user.first_name,
        'last_name': user.last_name,
        'username': user.username,
        'email': user.email,
        'roles_id': user.roles_id.__str__(),
        'districts_id': user.districts_id.__str__(),
    }

    access_token = create_access_token(identity=user.username, expires_delta=datetime.timedelta(minutes=30),
                                       user_claims=payload)
    return jsonify(
        access_token=access_token,
        status=Status.status_successfully_processed().__dict__)


@bpp.route('/renew', methods=['GET'])
@jwt_required
def refresh():
    current_user = get_jwt_identity()
    payload = {
        'id': get_jwt_claims()['id'].__str__(),
        'first_name': get_jwt_claims()['first_name'],
        'last_name': get_jwt_claims()['last_name'],
        'username': get_jwt_claims()['username'],
        'email': get_jwt_claims()['email'],
        'roles_id': get_jwt_claims()['roles_id'].__str__(),
        'districts_id': get_jwt_claims()['districts_id'].__str__()
    }
    access_token = create_access_token(identity=current_user, expires_delta=datetime.timedelta(minutes=30),
                                       user_claims=payload)
    return jsonify(
        access_token=access_token,
        status=Status.status_successfully_processed().__dict__)


@bpp.route('/alter_your_password', methods=['PUT'])
@jwt_required
def alter_your_password():
    user_id = get_jwt_claims()['id']

    request_json = request.get_json()
    schema = YourPasswordSchema()
    params = schema.load(request_json)

    controller = UserController(
        user=User(
            id=user_id,
            password_hash=generate_password_hash(params['new_password'], method='sha256'),
        ))

    controller.alter_password()

    return jsonify(
        data=UserController.get_one_details(controller.user.id),
        status=Status.status_update_success().__dict__)








