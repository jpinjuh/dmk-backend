from flask import request, jsonify

from .controller import RoleController
from ... import bpp, Role, FlaskProjectLogException
from ...general import Status, obj_to_dict
from ...general.route_decorators import allow_access
from ...schema import RoleSchema

@bpp.route('/role', methods=['POST'])
@allow_access
def create_role():
    request_json = request.get_json()
    schema = RoleSchema(exclude=('id',))

    params = schema.load(request_json)

    controller = RoleController(
        role=Role(
            name=params['name']
        ))
    controller.create()

    return jsonify(
        data=obj_to_dict(controller.role),
        status=Status.status_successfully_inserted().__dict__)

@bpp.route('/role/<string:role_id>', methods=['PUT'])
@allow_access
def alter_role(role_id):
    request_json = request.get_json()
    schema = RoleSchema(exclude=('id',))

    params = schema.load(request_json)

    controller = RoleController(
        role=Role(
            id=role_id,
            name=params['name']
        ))
    controller.alter()

    return jsonify(
        data=obj_to_dict(controller.role),
        status=Status.status_update_success().__dict__)

@bpp.route('/role/<string:role_id>', methods=['DELETE'])
#@allow_access
def role_inactivate(role_id):
    controller = RoleController(
        role=Role(id=role_id))

    controller.inactivate()

    return jsonify(
        data=obj_to_dict(controller.role),
        status=Status.status_successfully_processed().__dict__)

@bpp.route('/role/activate', methods=['POST'])
#@allow_access
def role_activate():
    request_json = request.get_json()
    schema = RoleSchema(only=('id',))

    params = schema.load(request_json)
    controller = RoleController(
        role=Role(id=params['id']))

    controller.activate()

    return jsonify(
        data=obj_to_dict(controller.role),
        status=Status.status_successfully_processed().__dict__)

@bpp.route('/role/<string:role_id>', methods=['GET'])
#@allow_access
def get_one_role(role_id):
    controller = RoleController.get_one_details(role_id)

    if controller is None:
        raise FlaskProjectLogException(Status.status_role_not_exist())

    return jsonify(
        data=controller,
        status=Status.status_successfully_processed().__dict__)


@bpp.route('/role/autocomplete', methods=['POST'])
#@allow_access
def role_autocomplete():
    request_json = request.get_json()
    search = request_json.get('search', None)

    data = RoleController.list_autocomplete(search)

    return jsonify(
        data=data,
        status=Status.status_successfully_processed().__dict__)


@bpp.route('/role', methods=['GET'])
#@allow_access
def get_roles():
    start = request.args.get('start', 0, int)
    limit = request.args.get('limit', 20, int)
    name = request.args.get('name', None, str)

    pagination_result = RoleController.get_list_pagination(
        start=start, limit=limit, name=name)

    return jsonify(pagination_result)

@bpp.route('/roles', methods=['GET'])
@allow_access
def get_all_roles():
    data = RoleController.get_all()
    return jsonify(data)