from flask import request, jsonify
from .controller import ListController
#from ...flask_jwt import JWT, current_identity,jwt_required
from ...flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity, get_jwt_claims
)
from ... import bpp, List, FlaskProjectLogException
from ...general import Status, obj_to_dict
from ...general.route_decorators import allow_access
from ...schema import ListSchema


@bpp.route('/list', methods=['POST'])
@jwt_required
#@allow_access
def create_list():
    request_json = request.get_json()
    schema = ListSchema(exclude=('id',))

    params = schema.load(request_json)

    controller = ListController(
        list=List(
            name=params['name']
        ))
    controller.create()

    return jsonify(
        data=obj_to_dict(controller.list),
        status=Status.status_successfully_inserted().__dict__)


@bpp.route('/list', methods=['GET'])
@jwt_required
#@allow_access
def get_lists():
    start = request.args.get('start', 0, int)
    limit = request.args.get('limit', 10, int)
    name = request.args.get('name', None, str)

    pagination_result = ListController.get_list_pagination(
        start=start, limit=limit, name=name)

    return jsonify(pagination_result)

