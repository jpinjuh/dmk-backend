from flask import request, jsonify
#from ...flask_jwt import JWT, jwt_required, current_identity
from ...flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity, get_jwt_claims
)
from .controller import PrivilegeController
from ... import bpp, Privilege, FlaskProjectLogException
from ...general import Status, obj_to_dict
from ...general.route_decorators import allow_access
from ...schema import PrivilegeSchema


@bpp.route('/privilege', methods=['POST'])
@jwt_required
#@allow_access
def create_privilege():
    request_json = request.get_json()
    schema = PrivilegeSchema(exclude=('id',))

    params = schema.load(request_json)

    controller = PrivilegeController(
        privilege=Privilege(
            roles_id=params['role']['id'],
            permissions_id=params['permission']['id']
        ))

    controller.create()

    return jsonify(
        data=PrivilegeController.get_one_details(controller.privilege.id),
        status=Status.status_successfully_inserted().__dict__)


@bpp.route('/privilege/<string:privilege_id>', methods=['PUT'])
@jwt_required
#@allow_access
def privilege_user(privilege_id):
    request_json = request.get_json()
    schema = PrivilegeSchema(exclude=('id',))

    params = schema.load(request_json)

    controller = PrivilegeController(
        privilege=Privilege(
            id=privilege_id,
            roles_id=params['role']['id'],
            permissions_id=params['permission']['id']
        ))
    controller.alter()

    return jsonify(
        data=obj_to_dict(controller.privilege),
        status=Status.status_update_success().__dict__)


@bpp.route('/privilege/<string:privilege_id>', methods=['DELETE'])
@jwt_required
#@allow_access
def privilege_inactivate(privilege_id):
    controller = PrivilegeController(
        privilege=Privilege(id=privilege_id))

    controller.inactivate()

    return jsonify(
        data=obj_to_dict(controller.privilege),
        status=Status.status_successfully_processed().__dict__)


@bpp.route('/privilege/activate', methods=['POST'])
@jwt_required
#@allow_access
def privilege_activate():
    request_json = request.get_json()
    schema = PrivilegeSchema(only=('id',))

    params = schema.load(request_json)
    controller = PrivilegeController(
        privilege=Privilege(id=params['id']))

    controller.activate()

    return jsonify(
        data=obj_to_dict(controller.privilege),
        status=Status.status_successfully_processed().__dict__)


@bpp.route('/privilege/<string:privilege_id>', methods=['GET'])
@jwt_required
#@allow_access
def get_one_privilege(privilege_id):
    controller = PrivilegeController.get_one_details(privilege_id)

    if controller is None:
        raise FlaskProjectLogException(Status.status_privilege_not_exist())

    return jsonify(
        data=controller,
        status=Status.status_successfully_processed().__dict__)


@bpp.route('/privilege/autocomplete', methods=['POST'])
@jwt_required
#@allow_access
def privilege_autocomplete():
    request_json = request.get_json()
    search = request_json.get('search', None)

    data = PrivilegeController.list_autocomplete(search)

    return jsonify(
        data=data,
        status=Status.status_successfully_processed().__dict__)


@bpp.route('/privilege', methods=['GET'])
@jwt_required
#@allow_access
def get_privileges():
    start = request.args.get('start', 0, int)
    limit = request.args.get('limit', 20, int)
    privilege_name = request.args.get('privilege_name', '', str)
    role_id = request.args.get('role_id', None, str)
    permission_id = request.args.get('permission_id', None, str)

    pagination_result = PrivilegeController.get_list_pagination(
        start=start, limit=limit, privilege_name=privilege_name,
        role_id=role_id, permission_id=permission_id)

    return jsonify(pagination_result)

@bpp.route('/role_permissions', methods=['GET', 'POST'])
@jwt_required
#@allow_access
def get_role_permissions():
    request_json = request.get_json()
    role_id = request_json.get('role_id')

    permissions = PrivilegeController.get_role_permissions(role_id)

    return jsonify(permissions)
