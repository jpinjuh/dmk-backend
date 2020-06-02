from flask import request, jsonify
from ...flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity, get_jwt_claims
)
from .controller import RegistryOfBaptismsController
from ..documents_controller.controller import DocumentController
from ..counter_controller.controller import CounterController
from ..persons_controller.controller import PersonController
from ... import bpp, RegistryOfBaptisms, FlaskProjectLogException, Document, Person, ListItem, Counter
from ...general import Status, obj_to_dict
from ...general.route_decorators import allow_access
from ...schema import PersonSchema, RegistryOfBaptismsSchema, DocumentSchema


@bpp.route('/registry_of_baptism', methods=['POST'])
@jwt_required
#@allow_access
def create_registry_of_baptism():
    request_json = request.get_json()
    schema = PersonSchema(exclude=('id',))

    params = schema.load({
        'first_name': request_json['first_name'],
        'last_name': request_json['last_name'],
        'maiden_name': request_json['maiden_name'],
        'birth_date': request_json['birth_date'],
        'identity_number': request_json['identity_number'],
        'father': request_json['father'],
        'mother': request_json['mother'],
        'district': request_json['district'],
        'religion': request_json['religion']
    })

    controller = PersonController(
        person=Person(
            first_name=params['first_name'],
            last_name=params['last_name'],
            maiden_name=params['maiden_name'],
            birth_date=params['birth_date'],
            identity_number=params['identity_number'],
            father_id=params['father']['id'],
            mother_id=params['mother']['id'],
            district=params['district']['id'],
            religion=params['religion']['id']
        ))
    controller.create()

    schema = DocumentSchema(exclude=('id', 'document_type', 'person', 'person2', 'user_created', ))
    params = schema.load({
        'act_date': request_json['act_date'],
        'act_performed': request_json['act_performed'],
        'document_number': request_json['document_number'],
        'volume': request_json['volume'],
        'year': request_json['year'],
        'page': request_json['page'],
        'number': request_json['number'],
        'district': request_json['district']
    })

    current_user = get_jwt_claims()['id']
    document_type_value = ListItem.query.filter_by(value='Matica krštenih').first()

    controller = DocumentController(
        document=Document(
            document_type=document_type_value.id,
            person_id=controller.person.id,
            act_date=params['act_date'],
            act_performed=params['act_performed']['id'],
            document_number='K - ' + CounterController.generate(Counter.counters['document_number']),
            district=params['district']['id'],
            volume=params['volume'],
            year=params['year'],
            page=params['page'],
            number=params['number'],
            user_created=current_user
        ))
    controller.create()

    schema = RegistryOfBaptismsSchema(exclude=('id', 'person'))
    params = schema.load({
        'best_man': request_json['best_man'],
        'name': request_json['first_name'],
        'surname': request_json['last_name'],
        'birth_date': request_json['birth_date'],
        'birth_place': request_json['birth_place'],
        'identity_number': request_json['identity_number'],
        'child': request_json['child']
    })

    controller = RegistryOfBaptismsController(
        baptism=RegistryOfBaptisms(
            id=controller.document.id,
            person_id=controller.document.person_id,
            best_man=params['best_man']['id'],
            name=params['name'],
            surname=params['surname'],
            birth_date=params['birth_date'],
            birth_place=params['birth_place']['id'],
            identity_number=params['identity_number'],
            child=params['child']['id']
        ))
    controller.create()

    return jsonify(
        data=RegistryOfBaptismsController.get_one_details(controller.baptism.id),
        status=Status.status_successfully_inserted().__dict__)







