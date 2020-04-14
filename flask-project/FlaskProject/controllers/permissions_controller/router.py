from flask import request, jsonify

from .controller import PermissionController
from ... import bpp, Permission, FlaskProjectLogException
from ...general import Status, obj_to_dict
from ...general.route_decorators import allow_access
from ...schema import PermissionSchema

@bpp.route('/permission', methods=['POST'])
#@allow_access
def create_permission():
    request_json = request.get_json()
    schema = PermissionSchema(exclude=('id',))

    params = schema.load(request_json)

    controller = PermissionController(
        permission=Permission(
            name=params['name'],
            route=params['route'],
            method=params['method']

        ))
    controller.create()

    return jsonify(
        data=obj_to_dict(controller.permission),
        status=Status.status_successfully_inserted().__dict__)

@bpp.route('/permission/<string:permission_id>', methods=['PUT'])
#@allow_access
def alter_permission(permission_id):
    request_json = request.get_json()
    schema = PermissionSchema(exclude=('id',))

    params = schema.load(request_json)

    controller = PermissionController(
        permission=Permission(
            id=permission_id,
            name=params['name'],
            route=params['route'],
            method=params['method']
        ))
    controller.alter()

    return jsonify(
        data=obj_to_dict(controller.permission),
        status=Status.status_update_success().__dict__)

@bpp.route('/permission/<string:permission_id>', methods=['DELETE'])
#@allow_access
def permission_inactivate(permission_id):
    controller = PermissionController(
        permission=Permission(id=permission_id))

    controller.inactivate()

    return jsonify(
        data=obj_to_dict(controller.permission),
        status=Status.status_successfully_processed().__dict__)

@bpp.route('/permission/activate', methods=['POST'])
#@allow_access
def permission_activate():
    request_json = request.get_json()
    schema = PermissionSchema(only=('id',))

    params = schema.load(request_json)
    controller = PermissionController(
        permission=Permission(id=params['id']))

    controller.activate()

    return jsonify(
        data=obj_to_dict(controller.permission),
        status=Status.status_successfully_processed().__dict__)

@bpp.route('/permission/<string:permission_id>', methods=['GET'])
#@allow_access
def get_one_permission(permission_id):
    controller = PermissionController.get_one_details(permission_id)

    if controller is None:
        raise FlaskProjectLogException(Status.status_permission_not_exist())

    return jsonify(
        data=controller,
        status=Status.status_successfully_processed().__dict__)


@bpp.route('/permission/autocomplete', methods=['POST'])
#@allow_access
def permission_autocomplete():
    request_json = request.get_json()
    search = request_json.get('search', None)
    data = PermissionController.list_autocomplete(search)

    return jsonify(
        data=data,
        status=Status.status_successfully_processed().__dict__)

@bpp.route('/permission', methods=['GET'])
#@allow_access
def get_permission():
    start = request.args.get('start', 0, int)
    limit = request.args.get('limit', 20, int)
    name = request.args.get('name', None, str)

    pagination_result = PermissionController.get_list_pagination(
        start=start, limit=limit, name=name)

    return jsonify(pagination_result)


