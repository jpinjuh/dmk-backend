from flask import request, jsonify, make_response, current_app, Flask
from ...flask_jwt.flask_jwt import JWT, jwt_required, current_identity, JWTError
from ...flask_jwt_extended.flask_jwt_extended import (
    JWTManager, create_access_token,
    jwt_refresh_token_required, create_refresh_token,
    get_jwt_identity, fresh_jwt_required
)
from ...controllers.users_controller.controller import UserController
from ... import bpp, User, FlaskProjectLogException
from ...general import Status, authenticate, identity
from ...general.route_decorators import allow_access
from ...schema import UserSchema
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime
import uuid


@bpp.route('/login', methods=('POST',))
def login():
    data = request.get_json()
    user = User.authenticate(**data)

    if not user:
        return jsonify(
            message='Invalid credentials',
            status=Status.status_unsuccessfully_processed().__dict__)

    payload = {
        'identity': user.id.__str__(),
        'first_name': user.first_name,
        'last_name': user.last_name,
        'username': user.username,
        'email': user.email,
        'roles_id': user.roles_id.__str__(),
        'iat': datetime.datetime.utcnow(),
        'nbf': 3000,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
    }
    token = jwt.encode(payload, current_app.config['JWT_SECRET_KEY'])

    return jsonify(
        access_token=token.decode('UTF-8'),
        status=Status.status_successfully_processed().__dict__)


"""
@bpp.route('/renew', methods=['POST', 'GET'])
@jwt_required()
def refresh():

    return %s current_identity
    #user = User.query.filter(id=current_identity['id']).first()
    #data = {'user': user.id}
    #username = data.get(current_app.config.get('JWT_AUTH_USERNAME_KEY'), None)
    #criterion = [username, len(data) == 1]
"""
"""
    if not all(criterion):
        raise JWTError('Bad Request', 'Invalid credentials')

    #identity = _jwt.authentication_callback(user_id)
    identity.update({
        'first_name': current_identity['first_name'],
        'last_name': current_identity['last_name'],
        'username': current_identity['username']
    })

    if identity:
        access_token = _jwt.jwt_encode_callback(identity, current_identity['expiration_delta'])
        identity['user'] = user
        return _jwt.auth_response_callback(access_token, identity)
    else:
        raise JWTError('Bad Request', 'Invalid credentials')"""


"""
@bpp.route('/renew', methods=['POST', 'GET'])
@jwt_required()
def refresh():
    verify_jwt()
    payload = jwt.payload_callback(current_user)
    new_token = jwt.encode_callback(payload)
    return jwt.response_callback(new_token)"""

@bpp.route('/refresh', methods=['POST'])
@jwt_required()
def refresh():
    current_user = current_identity
    #current_user = User.query.filter_by(id=current_identity['id']).first()
    return current_identity.first_name
    #new_token = create_access_token(identity=current_user, fresh=False)
    #ret = {'access_token': new_token}
    #return jsonify(ret), 200
