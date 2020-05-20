from flask import request, jsonify
from .controller import PersonController
#from ...flask_jwt import JWT, current_identity,jwt_required
from ...flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity, get_jwt_claims
)
from ... import bpp, Person, FlaskProjectLogException
from ...general import Status, obj_to_dict
from ...general.route_decorators import allow_access
from ...schema import PersonSchema


@bpp.route('/person', methods=['POST'])
@jwt_required
#@allow_access
def create_person():
    request_json = request.get_json()
    schema = PersonSchema(exclude=('id',))

    params = schema.load(request_json)

    controller = PersonController(
        person=Person(
            first_name=params['first_name'],
            last_name=params['last_name'],
            maiden_name=params['maiden_name'],
            birth_date=params['birth_date'],
            identity_number=params['identity_number'],
            father_id=params['father_id'],
            mother_id=params['mother_id'],
            district=params['district'],
            religion=params['religion']
        ))
    controller.create()

    return jsonify(
        data=obj_to_dict(controller.person),
        status=Status.status_successfully_inserted().__dict__)

@bpp.route('/person/<string:person_id>', methods=['GET'])
@jwt_required
#@allow_access
def get_one_person(person_id):
    controller = PersonController.get_one_details(person_id)

    if controller is None:
        raise FlaskProjectLogException(Status.status_person_not_exist())

    return jsonify(
        data=controller,
        status=Status.status_successfully_processed().__dict__)

@bpp.route('/person', methods=['GET'])
@jwt_required
#@allow_access
def get_persons():
    start = request.args.get('start', 0, int)
    limit = request.args.get('limit', 10, int)

    first_name = request.args.get('first_name', '', str)
    last_name = request.args.get('last_name', '', str)
    maiden_name = request.args.get('maiden_name', '', str)
    birth_date = request.args.get('birth_date', '', str)
    identity_number = request.args.get('identity_number', '', str)
    father_id = request.args.get('father_id', None, str)
    mother_id = request.args.get('mother_id', None, str)
    district = request.args.get('district', None, str)
    religion = request.args.get('religion', None, str)

    pagination_result = PersonController.get_person_pagination(
        start=start, limit=limit, first_name=first_name, last_name=last_name,
        maiden_name=maiden_name, birth_date=birth_date, identity_number=identity_number,
        father_id=father_id, mother_id=mother_id, district=district, religion=religion)

    return jsonify(pagination_result)