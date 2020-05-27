from flask import request, jsonify
from .controller import PersonController
from ..personsHistory_controller.controller import PersonsHistoryController
#from ...flask_jwt import JWT, current_identity,jwt_required
from ...flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity, get_jwt_claims
)
from ... import bpp, Person, FlaskProjectLogException
from ...general import Status, obj_to_dict
from ...general.route_decorators import allow_access
from ...schema import PersonSchema
import datetime
from sqlalchemy.sql import func


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
            maiden_name=params.get('maiden_name', None),
            birth_date=params['birth_date'],
            identity_number=params['identity_number'],
            domicile=params['domicile'],
            father_id=params['father']['id'],
            mother_id=params['mother']['id'],
            district=params['district']['id'],
            religion=params['religion']['id']
        ))
    controller.create()

    return jsonify(
        data=PersonController.get_one_details(controller.person.id),
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


@bpp.route('/person/autocomplete', methods=['POST'])
@jwt_required
#@allow_access
def person_autocomplete():
    request_json = request.get_json()
    search = request_json.get('search', None)

    data = PersonController.list_autocomplete(search)

    return jsonify(
        data=data,
        status=Status.status_successfully_processed().__dict__)


@bpp.route('/person/search', methods=['POST'])
@jwt_required
#@allow_access
def search_persons():
    request_json = request.get_json()

    start = request_json.get('start', 0)
    limit = request_json.get('limit', 10)

    first_name = request_json.get('first_name', None)
    last_name = request_json.get('last_name', None)
    birth_date = request_json.get('birth_date', None)
    birth_place = request_json.get('birth_place', None)
    identity_number = request_json.get('identity_number', None)

    pagination_result = PersonController.get_list_search(
        start=start, limit=limit, first_name=first_name, last_name=last_name,
        birth_date=birth_date, birth_place=birth_place, identity_number=identity_number)

    return jsonify(pagination_result)


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

    pagination_result = PersonController.get_list_pagination(
        start=start, limit=limit, first_name=first_name, last_name=last_name,
        maiden_name=maiden_name, birth_date=birth_date, identity_number=identity_number,
        father_id=father_id, mother_id=mother_id, district=district, religion=religion)

    return jsonify(pagination_result)