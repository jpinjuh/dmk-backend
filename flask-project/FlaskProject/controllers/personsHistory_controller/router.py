import controller as controller
from flask import request, jsonify
from ...flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity, get_jwt_claims
)
from . controller import PersonsHistoryController
from ... import bpp, PersonsHistory, FlaskProjectLogException, Person
from ...general import Status, obj_to_dict
from ...general.route_decorators import allow_access
from ...schema import PersonsHistorySchema

""""
@bpp.route('/persons_history', methods=['POST'])
@jwt_required
#@allow_access
def create_persons_history():
    request_json = request.get_json()
    schema = PersonsHistorySchema(exclude=('id',))

    params = schema.load(request_json)

    current_user = get_jwt_claims()['id']
    #person = PersonController.get_one_details(person_id)

    controller = PersonsHistoryController(
        personsHistory=PersonsHistory(
            first_name=person.first_name,
            last_name=controller.person.last_name,
            maiden_name=controller.person.maiden_name,
            birth_date=controller.person.birth_date,
            identity_number=controller.person.identity_number,
            father_id=controller.person.father_id,
            mother_id=controller.person.mother_id,
            district=controller.person.district,
            religion=controller.person.religion,
            person=controller.person.id,
            user_created=current_user
        ))
    controller.create()

    return jsonify(
        data=PersonsHistoryController.get_one_details(controller.personsHistory.id),
        status=Status.status_successfully_inserted().__dict__)
"""
@bpp.route('/persons_history', methods=['GET'])
@jwt_required
#@allow_access
def get_persons_history():
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
    person = request.args.get('person', None, str)
    user_created = request.args.get('user_created', None, str)

    pagination_result = PersonsHistoryController.get_list_pagination(
        start=start, limit=limit, first_name=first_name, last_name=last_name,
        maiden_name=maiden_name, birth_date=birth_date, identity_number=identity_number,
        father_id=father_id, mother_id=mother_id, district=district, religion=religion,
        person=person, user_created=user_created)

    return jsonify(pagination_result)






