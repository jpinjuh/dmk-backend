from flask import request, jsonify
from ...flask_jwt_extended import jwt_required
from .controller import DistrictController
from ... import bpp, District, FlaskProjectLogException
from ...general import Status, obj_to_dict
from ...general.route_decorators import allow_access
from ...schema import DistrictSchema


@bpp.route('/district', methods=['POST'])
@jwt_required
#@allow_access
def create_district():
    request_json = request.get_json()
    schema = DistrictSchema(exclude=('id',))

    params = schema.load(request_json)

    controller = DistrictController(
        district=District(
            name=params['name'],
            address=params['address'],
            city_id=params['city']['id'],
            archdiocese_id=params['archdiocese']['id']
        ))

    controller.create()

    return jsonify(
        data=DistrictController.get_one_details(controller.district.id),
        status=Status.status_successfully_inserted().__dict__)


@bpp.route('/district/<string:district_id>', methods=['PUT'])
@jwt_required
#@allow_access
def alter_district(district_id):
    request_json = request.get_json()
    schema = DistrictSchema(exclude=('id',))

    params = schema.load(request_json)

    controller = DistrictController(
        district=District(
            id=district_id,
            name=params['name'],
            address=params['address'],
            city_id=params['city']['id'],
            archdiocese_id=params['archdiocese']['id']
        ))
    controller.alter()

    return jsonify(
        data=DistrictController.get_one_details(controller.district.id),
        status=Status.status_update_success().__dict__)


@bpp.route('/district/<string:district_id>', methods=['DELETE'])
@jwt_required
#@allow_access
def district_inactivate(district_id):
    controller = DistrictController(
        district=District(id=district_id))

    controller.inactivate()

    return jsonify(
        data=obj_to_dict(controller.district),
        status=Status.status_successfully_processed().__dict__)


@bpp.route('/district/activate', methods=['POST'])
@jwt_required
#@allow_access
def district_activate():
    request_json = request.get_json()
    schema = DistrictSchema(only=('id',))

    params = schema.load(request_json)
    controller = DistrictController(
        district=District(id=params['id']))

    controller.activate()

    return jsonify(
        data=obj_to_dict(controller.district),
        status=Status.status_successfully_processed().__dict__)


@bpp.route('/district/<string:district_id>', methods=['GET'])
@jwt_required
#@allow_access
def get_one_district(district_id):
    controller = DistrictController.get_one_details(district_id)

    if controller is None:
        raise FlaskProjectLogException(Status.status_district_not_exist())

    return jsonify(
        data=controller,
        status=Status.status_successfully_processed().__dict__)


@bpp.route('/district/autocomplete', methods=['POST'])
@jwt_required
#@allow_access
def district_autocomplete():
    request_json = request.get_json()
    search = request_json.get('search', None)

    data = DistrictController.list_autocomplete(search)

    return jsonify(
        data=data,
        status=Status.status_successfully_processed().__dict__)


@bpp.route('/district/search', methods=['POST'])
@jwt_required
#@allow_access
def district_search():
    request_json = request.get_json()
    search = request_json.get('search', None)

    data = DistrictController.list_search(search)

    return jsonify(
        data=data,
        status=Status.status_successfully_processed().__dict__)

@bpp.route('/district', methods=['GET'])
@jwt_required
#@allow_access
def get_districts():
    start = request.args.get('start', 0, int)
    limit = request.args.get('limit', 10, int)

    district_name = request.args.get('district_name', '', str)
    address = request.args.get('address', '', str)
    city_id = request.args.get('city_id', None, str)
    archdiocese_id = request.args.get('archdiocese_id', None, str)

    pagination_result = DistrictController.get_list_pagination(
        start=start, limit=limit, district_name=district_name, address=address,
        city_id=city_id, archdiocese_id= archdiocese_id)

    return jsonify(pagination_result)