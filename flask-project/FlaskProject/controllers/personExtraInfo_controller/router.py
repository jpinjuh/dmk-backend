from flask import request, jsonify
from .controller import PersonExtraInfoController
from ...flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity, get_jwt_claims
)
from ... import bpp, Person, FlaskProjectLogException, PersonExtraInfo
from ...general import Status, obj_to_dict
from ...general.route_decorators import allow_access
from ...schema import PersonExtraInfoSchema
import datetime
from sqlalchemy.sql import func


@bpp.route('/person_extra_info', methods=['POST'])
@jwt_required
#@allow_access
def create_person_extra_info():
    request_json = request.get_json()
    schema = PersonExtraInfoSchema(exclude=('id',))
    params = schema.load(request_json)

    controller = PersonExtraInfoController(
        extra_info=PersonExtraInfo(
            person_id=params['person_id']['id'],
            baptism_district=params['baptism_district']['id'],
            baptism_date=params['baptism_date'],
            parents_canonically_married=params['parents_canonically_married']['id']
        ))
    controller.create()

    return jsonify(
        data=PersonExtraInfoController.get_one_details(controller.extra_info.id),
        status=Status.status_successfully_inserted().__dict__)
