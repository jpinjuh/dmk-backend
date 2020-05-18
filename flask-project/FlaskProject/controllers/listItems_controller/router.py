from flask import request, jsonify
from .controller import ListItemController
#from ...flask_jwt import JWT, current_identity,jwt_required
from ...flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity, get_jwt_claims
)
from ... import bpp, ListItem, List, FlaskProjectLogException
from ...general import Status, obj_to_dict
from ...general.route_decorators import allow_access
from ...schema import ListItemSchema


@bpp.route('/listItem', methods=['POST'])
@jwt_required
#@allow_access
def create_list_item():
    request_json = request.get_json()
    schema = ListItemSchema(exclude=('id',))

    params = schema.load(request_json)

    controller = ListItemController(
        list_item=ListItem(
            value=params['value'],
            description=params['description'],
            list_id=params['list']['id']
        ))
    controller.create()

    return jsonify(
        data=obj_to_dict(controller.list_item),
        status=Status.status_successfully_inserted().__dict__)


@bpp.route('/listItem', methods=['GET'])
@jwt_required
#@allow_access
def get_list_items():
    start = request.args.get('start', 0, int)
    limit = request.args.get('limit', 10, int)

    list_value = request.args.get('list_value', '', str)
    description = request.args.get('description', '', str)
    list_id = request.args.get('list_id', None, str)

    pagination_result = ListItemController.get_list_pagination(
        start=start, limit=limit, list_value=list_value, description=description,
        list_id=list_id)

    return jsonify(pagination_result)

