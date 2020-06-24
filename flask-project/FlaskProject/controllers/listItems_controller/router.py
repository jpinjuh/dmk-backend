from flask import request, jsonify
from .controller import ListItemController
from ...flask_jwt_extended import (
    jwt_required, get_jwt_claims
)
from ... import bpp, ListItem
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
            auxiliary_description=params['auxiliary_description'],
            list_id=params['list']['id']
        ))
    controller.create()

    return jsonify(
        data=obj_to_dict(controller.list_item),
        status=Status.status_successfully_inserted().__dict__)


@bpp.route('/listItem', methods=['GET'])
@jwt_required
#@allow_access
def get_all_list_items():
    start = request.args.get('start', 0, int)
    limit = request.args.get('limit', 10, int)

    list_value = request.args.get('list_value', '', str)
    description = request.args.get('description', '', str)
    auxiliary_description = request.args.get('auxiliary_description', '', str)
    list_id = request.args.get('list_id', None, str)

    pagination_result = ListItemController.get_list_pagination(
        start=start, limit=limit, list_value=list_value, description=description,
        auxiliary_description=auxiliary_description, list_id=list_id)

    return jsonify(pagination_result)


@bpp.route('/listItems/<string:list_id>', methods=['GET'])
@jwt_required
#@allow_access
def get_list_items(list_id):
    current_user_district = get_jwt_claims()['districts_id']
    if list_id:
        data = ListItemController.get_list_items(list_id, current_user_district)

        return jsonify(
            data=data,
            status=Status.status_successfully_processed().__dict__)


