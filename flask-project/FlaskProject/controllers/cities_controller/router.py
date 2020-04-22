from flask import request, jsonify
#from ...flask_jwt import JWT, jwt_required, current_identity
from ...flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity, get_jwt_claims
)
from .controller import CityController
from ... import bpp, City, FlaskProjectLogException
from ...general import Status, obj_to_dict
from ...general.route_decorators import allow_access
from ...schema import CitySchema


@bpp.route('/city', methods=['POST'])
@jwt_required
#@allow_access
def create_city():
    request_json = request.get_json()
    schema = CitySchema(exclude=('id',))

    params = schema.load(request_json)

    controller = CityController(
        city=City(
            name=params['name'],
            state_id=params['state']['id']
        ))

    controller.create()

    return jsonify(
        data=CityController.get_one_details(controller.city.id),
        status=Status.status_successfully_inserted().__dict__)

@bpp.route('/city/<string:city_id>', methods=['PUT'])
@jwt_required
#@allow_access
def alter_city(city_id):
    request_json = request.get_json()
    schema = CitySchema(exclude=('id',))

    params = schema.load(request_json)

    controller = CityController(
        city=City(
            id=city_id,
            name=params['name'],
            state_id=params['state']['id']
        ))
    controller.alter()

    return jsonify(
        data=obj_to_dict(controller.city),
        status=Status.status_update_success().__dict__)

@bpp.route('/city/<string:city_id>', methods=['DELETE'])
@jwt_required
#@allow_access
def city_inactivate(city_id):
    controller = CityController(
        city=City(id=city_id))

    controller.inactivate()

    return jsonify(
        data=obj_to_dict(controller.city),
        status=Status.status_successfully_processed().__dict__)

@bpp.route('/city/activate', methods=['POST'])
@jwt_required
#@allow_access
def city_activate():
    request_json = request.get_json()
    schema = CitySchema(only=('id',))

    params = schema.load(request_json)
    controller = CityController(
        city=City(id=params['id']))

    controller.activate()

    return jsonify(
        data=obj_to_dict(controller.city),
        status=Status.status_successfully_processed().__dict__)

@bpp.route('/city/<string:city_id>', methods=['GET'])
@jwt_required
#@allow_access
def get_one_city(city_id):
    controller = CityController.get_one_details(city_id)

    if controller is None:
        raise FlaskProjectLogException(Status.status_city_not_exist())

    return jsonify(
        data=controller,
        status=Status.status_successfully_processed().__dict__)


@bpp.route('/city/autocomplete', methods=['POST'])
@jwt_required
#@allow_access
def city_autocomplete():
    request_json = request.get_json()
    search = request_json.get('search', None)

    data = CityController.list_autocomplete(search)

    return jsonify(
        data=data,
        status=Status.status_successfully_processed().__dict__)


@bpp.route('/city', methods=['GET'])
@jwt_required
#@allow_access
def get_cities():
    start = request.args.get('start', 0, int)
    limit = request.args.get('limit', 20, int)

    city_name = request.args.get('city_name', '', str)
    state_id = request.args.get('state_id', None, str)

    pagination_result = CityController.get_list_pagination(
        start=start, limit=limit, city_name=city_name,
        state_id=state_id)

    return jsonify(pagination_result)
