from flask import request, jsonify
from ...flask_jwt import JWT, jwt_required, current_identity
from .controller import CityController
from ... import bpp, City, FlaskProjectLogException
from ...general import Status
from ...general.route_decorators import allow_access
from ...schema import CitySchema


@bpp.route('/city', methods=['POST'])
@jwt_required()
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


@bpp.route('/city/<string:city_id>', methods=['GET'])
@jwt_required()
#@allow_access
def get_one_city(city_id):
    controller = CityController.get_one_details(city_id)

    if controller is None:
        raise FlaskProjectLogException(Status.status_city_not_exist())

    return jsonify(
        data=controller,
        status=Status.status_successfully_processed().__dict__)


@bpp.route('/city/autocomplete', methods=['POST'])
@jwt_required()
#@allow_access
def city_autocomplete():
    request_json = request.get_json()
    search = request_json.get('search', None)

    data = CityController.list_autocomplete(search)

    return jsonify(
        data=data,
        status=Status.status_successfully_processed().__dict__)


@bpp.route('/city', methods=['GET'])
@jwt_required()
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
