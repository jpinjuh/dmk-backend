from flask import request, jsonify
from ...flask_jwt.flask_jwt import JWT, jwt_required, current_identity
from .controller import UserController
from ... import bpp, User, FlaskProjectLogException
from ...general import Status
from ...general.route_decorators import allow_access
from ...schema import UserSchema
from werkzeug.security import generate_password_hash, check_password_hash

@bpp.route('/user', methods=['POST'])
@jwt_required()
#@allow_access
def create_user():
    request_json = request.get_json()
    schema = UserSchema(exclude=('id',))

    params = schema.load(request_json)

    controller = UserController(
        user=User(
            first_name=params['first_name'],
            last_name=params['last_name'],
            username=params['username'],
            email=params['email'],
            password_hash=generate_password_hash(params['password_hash'], method='sha256'),
            roles_id=params['role']['id'],
            districts_id=params['district']['id']
        ))

    controller.create()

    return jsonify(
        data=UserController.get_one_details(controller.user.id),
        status=Status.status_successfully_inserted().__dict__)


@bpp.route('/user/<string:user_id>', methods=['GET'])
@jwt_required()
#@allow_access
def get_one_user(user_id):
    controller = UserController.get_one_details(user_id)

    if controller is None:
        raise FlaskProjectLogException(Status.status_user_not_exist())

    return jsonify(
        data=controller,
        status=Status.status_successfully_processed().__dict__)


@bpp.route('/user/autocomplete', methods=['POST'])
@jwt_required()
#@allow_access
def user_autocomplete():
    request_json = request.get_json()
    search = request_json.get('search', None)

    data = UserController.list_autocomplete(search)

    return jsonify(
        data=data,
        status=Status.status_successfully_processed().__dict__)


@bpp.route('/user', methods=['GET'])
@jwt_required()
#@allow_access
def get_users():
    start = request.args.get('start', 0, int)
    limit = request.args.get('limit', 20, int)

    first_name = request.args.get('first_name', '', str)
    last_name = request.args.get('last_name', '', str)
    username = request.args.get('username', '', str)
    email = request.args.get('email', '', str)
    roles_id = request.args.get('roles_id', None, str)
    districts_id = request.args.get('districts_id', None, str)

    pagination_result = UserController.get_list_pagination(
        start=start, limit=limit, first_name=first_name, last_name=last_name,
        username=username, email=email, roles_id=roles_id, districts_id=districts_id)

    return jsonify(pagination_result)
