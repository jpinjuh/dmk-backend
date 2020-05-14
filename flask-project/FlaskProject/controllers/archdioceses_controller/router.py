from flask import request, jsonify
#from ...flask_jwt import JWT, current_identity, jwt_required
from ...flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity, get_jwt_claims
)
from .controller import ArchdioceseController
from ... import bpp, Archdiocese, FlaskProjectLogException
from ...general import Status, obj_to_dict
from ...general.route_decorators import allow_access
from ...schema import ArchdioceseSchema


@bpp.route('/archdiocese', methods=['POST'])
@jwt_required
#@allow_access
def create_archdiocese():
    request_json = request.get_json()
    schema = ArchdioceseSchema(exclude=('id',))

    params = schema.load(request_json)

    controller = ArchdioceseController(
        archdiocese=Archdiocese(
            name=params['name']
        ))
    controller.create()

    return jsonify(
        data=obj_to_dict(controller.archdiocese),
        status=Status.status_successfully_inserted().__dict__)


@bpp.route('/archdiocese/<string:archdiocese_id>', methods=['PUT'])
@jwt_required
#@allow_access
def alter_archdiocese(archdiocese_id):
    request_json = request.get_json()
    schema = ArchdioceseSchema(exclude=('id',))

    params = schema.load(request_json)

    controller = ArchdioceseController(
        archdiocese=Archdiocese(
            id=archdiocese_id,
            name=params['name']
        ))
    controller.alter()

    return jsonify(
        data=obj_to_dict(controller.archdiocese),
        status=Status.status_update_success().__dict__)


@bpp.route('/archdiocese/<string:archdiocese_id>', methods=['DELETE'])
@jwt_required
#@allow_access
def archdiocese_inactivate(archdiocese_id):
    controller = ArchdioceseController(
        archdiocese=Archdiocese(id=archdiocese_id))

    controller.inactivate()

    return jsonify(
        data=obj_to_dict(controller.archdiocese),
        status=Status.status_successfully_processed().__dict__)


@bpp.route('/archdiocese/activate', methods=['POST'])
@jwt_required
#@allow_access
def archdiocese_activate():
    request_json = request.get_json()
    schema = ArchdioceseSchema(only=('id',))

    params = schema.load(request_json)
    controller = ArchdioceseController(
        archdiocese=Archdiocese(id=params['id']))

    controller.activate()

    return jsonify(
        data=obj_to_dict(controller.archdiocese),
        status=Status.status_successfully_processed().__dict__)


@bpp.route('/archdiocese/<string:archdiocese_id>', methods=['GET'])
@jwt_required
#@allow_access
def get_one_archdiocese(archdiocese_id):
    controller = ArchdioceseController.get_one_details(archdiocese_id)

    if controller is None:
        raise FlaskProjectLogException(Status.status_archdiocese_not_exist())

    return jsonify(
        data=controller,
        status=Status.status_successfully_processed().__dict__)


@bpp.route('/archdiocese/autocomplete', methods=['POST'])
@jwt_required
#@allow_access
def archdiocese_autocomplete():
    request_json = request.get_json()
    search = request_json.get('search', None)

    data = ArchdioceseController.list_autocomplete(search)

    return jsonify(
        data=data,
        status=Status.status_successfully_processed().__dict__)


@bpp.route('/archdiocese/search', methods=['POST'])
@jwt_required
#@allow_access
def archdiocese_search():
    request_json = request.get_json()
    search = request_json.get('search', None)

    data = ArchdioceseController.list_search(search)

    return jsonify(
        data=data,
        status=Status.status_successfully_processed().__dict__)


@bpp.route('/archdiocese', methods=['GET'])
@jwt_required
#@allow_access
def get_archdioceses():
    start = request.args.get('start', 0, int)
    limit = request.args.get('limit', 10, int)
    name = request.args.get('name', None, str)

    pagination_result = ArchdioceseController.get_list_pagination(
        start=start, limit=limit, name=name)

    return jsonify(pagination_result)


