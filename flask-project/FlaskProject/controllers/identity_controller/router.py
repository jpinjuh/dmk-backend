from flask import request, jsonify, current_app, make_response

from ...controllers.users_controller.controller import UserController
from ... import bpp, User, FlaskProjectLogException
from ...general import Status
from ...general.route_decorators import allow_access
from ...schema import UserSchema
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime

""""
@bpp.route('/login', methods=['GET', 'POST'])
def login():
    auth = request.authorization

    if not auth or not auth.username or not auth.password:
        return make_response('Could not verify!', 401, {'WWW-Authentication': 'Basic realm: "login required"'})

    user = User.query.filter_by(username=auth.username).first()

    if not user:
        return make_response('Could not verify!', 401, {'WWW-Authentication': 'Basic realm: "login required"'})

    if check_password_hash(user.password_hash, auth.password):
        token = jwt.encode(
            {'username': user.username, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)},
            current_app.config.get('JWT_SECRET_KEY'))
        return jsonify({'token': token.decode('UTF-8')})

    return make_response('Could not verify!', 401, {'WWW-Authentication': 'Basic realm: "login required"'})
"""

@bpp.route('/login', methods=('POST',))
def login():
    data = request.get_json()
    user = User.authenticate(**data)

    if not user:
        return jsonify({'message': 'Invalid credentials', 'authenticated': False}), 401

    token = jwt.encode({
        'sub': user.username,
        'iat': datetime.datetime.utcnow(),
        'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)},
        current_app.config['JWT_SECRET_KEY'])
    return jsonify({'token': token.decode('UTF-8')})