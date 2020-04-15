from flask import request, jsonify

from .controller import StateController
from ... import bpp, State, FlaskProjectLogException
from ...general import Status, obj_to_dict
from ...general.route_decorators import allow_access
from ...schema import StateSchema


@bpp.route('/state', methods=['POST'])
@allow_access
def create_state():
    request_json = request.get_json()
    schema = StateSchema(exclude=('id',))

    params = schema.load(request_json)

    controller = StateController(
        state=State(
            name=params['name']
        ))
    controller.create()

    return jsonify(
        data=obj_to_dict(controller.state),
        status=Status.status_successfully_inserted().__dict__)


@bpp.route('/state/<string:state_id>', methods=['PUT'])
@allow_access
def alter_state(state_id):
    request_json = request.get_json()
    schema = StateSchema(exclude=('id',))

    params = schema.load(request_json)

    controller = StateController(
        state=State(
            id=state_id,
            name=params['name']
        ))
    controller.alter()

    return jsonify(
        data=obj_to_dict(controller.state),
        status=Status.status_update_success().__dict__)


@bpp.route('/state/<string:state_id>', methods=['DELETE'])
@allow_access
def state_inactivate(state_id):
    controller = StateController(
        state=State(id=state_id))

    controller.inactivate()

    return jsonify(
        data=obj_to_dict(controller.state),
        status=Status.status_successfully_processed().__dict__)


@bpp.route('/state/activate', methods=['POST'])
@allow_access
def state_activate():
    request_json = request.get_json()
    schema = StateSchema(only=('id',))

    params = schema.load(request_json)
    controller = StateController(
        state=State(id=params['id']))

    controller.activate()

    return jsonify(
        data=obj_to_dict(controller.state),
        status=Status.status_successfully_processed().__dict__)


@bpp.route('/state/<string:state_id>', methods=['GET'])
@allow_access
def get_one_state(state_id):
    controller = StateController.get_one_details(state_id)

    if controller is None:
        raise FlaskProjectLogException(Status.status_state_not_exist())

    return jsonify(
        data=controller,
        status=Status.status_successfully_processed().__dict__)


@bpp.route('/state/autocomplete', methods=['POST'])
@allow_access
def state_autocomplete():
    request_json = request.get_json()
    search = request_json.get('search', None)

    data = StateController.list_autocomplete(search)

    return jsonify(
        data=data,
        status=Status.status_successfully_processed().__dict__)


@bpp.route('/state', methods=['GET'])
@allow_access
def get_states():
    start = request.args.get('start', 0, int)
    limit = request.args.get('limit', 20, int)
    name = request.args.get('name', None, str)

    pagination_result = StateController.get_list_pagination(
        start=start, limit=limit, name=name)

    return jsonify(pagination_result)


