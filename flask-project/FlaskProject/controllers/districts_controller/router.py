from flask import request, jsonify
from ...flask_jwt import JWT, jwt_required, current_identity
from .controller import DistrictController
from ... import bpp, District, FlaskProjectLogException
from ...general import Status
from ...general.route_decorators import allow_access
from ...schema import DistrictSchema


@bpp.route('/district', methods=['POST'])
@jwt_required()
#@allow_access
def create_district():
    request_json = request.get_json()
    schema = DistrictSchema(exclude=('id',))

    params = schema.load(request_json)

    controller = DistrictController(
        district=District(
            name=params['name'],
            city_id=params['city']['id']
        ))

    controller.create()

    return jsonify(
        data=DistrictController.get_one_details(controller.district.id),
        status=Status.status_successfully_inserted().__dict__)


@bpp.route('/district/<string:district_id>', methods=['GET'])
@jwt_required()
#@allow_access
def get_one_district(district_id):
    controller = DistrictController.get_one_details(district_id)

    if controller is None:
        raise FlaskProjectLogException(Status.status_district_not_exist())

    return jsonify(
        data=controller,
        status=Status.status_successfully_processed().__dict__)


@bpp.route('/district/autocomplete', methods=['POST'])
@jwt_required()
#@allow_access
def district_autocomplete():
    request_json = request.get_json()
    search = request_json.get('search', None)

    data = DistrictController.list_autocomplete(search)

    return jsonify(
        data=data,
        status=Status.status_successfully_processed().__dict__)


@bpp.route('/district', methods=['GET'])
@jwt_required()
#@allow_access
def get_districts():
    start = request.args.get('start', 0, int)
    limit = request.args.get('limit', 20, int)

    district_name = request.args.get('district_name', '', str)
    city_id = request.args.get('city_id', None, str)

    pagination_result = DistrictController.get_list_pagination(
        start=start, limit=limit, district_name=district_name,
        city_id=city_id)

    return jsonify(pagination_result)