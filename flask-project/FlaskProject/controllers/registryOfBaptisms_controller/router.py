from flask import request, jsonify
from ...flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity, get_jwt_claims
)
from .controller import RegistryOfBaptismsController
from ..documents_controller.controller import DocumentController
from ..counter_controller.controller import CounterController
from ..persons_controller.controller import PersonController
from ..notes_controller.controller import NoteController
from ... import bpp, RegistryOfBaptisms, FlaskProjectLogException, Document, Person, ListItem, Counter, Note
from ...general import Status, obj_to_dict
from ...general.route_decorators import allow_access
from ...schema import PersonSchema, RegistryOfBaptismsSchema, DocumentSchema, NoteSchema


@bpp.route('/registry_of_baptism', methods=['POST'])
@jwt_required
#@allow_access
def create_registry_of_baptism():
    request_json = request.get_json()
    schema = PersonSchema(exclude=('id',))

    params = schema.load({
        'first_name': request_json['first_name'],
        'last_name': request_json['last_name'],
        'birth_date': request_json['birth_date'],
        'birth_place': request_json['birth_place'],
        'identity_number': request_json['identity_number'],
        'domicile': request_json.get('domicile', ''),
        'father': request_json['father'],
        'mother': request_json['mother'],
        'district': request_json['district'],
        'religion': request_json['religion']
    })

    controller = PersonController(
        person=Person(
            first_name=params['first_name'],
            last_name=params['last_name'],
            birth_date=params['birth_date'],
            birth_place=params['birth_place']['id'],
            identity_number=params['identity_number'],
            domicile=params.get('domicile', None),
            father_id=params['father']['id'],
            mother_id=params['mother']['id'],
            district=params['district']['id'],
            religion=params['religion']['id']
        ))
    controller.create()

    schema = DocumentSchema(exclude=('id', 'document_type', 'person', 'person2', 'user_created', 'document_number'))
    params = schema.load({
        'act_date': request_json['act_date'],
        'act_performed': request_json['act_performed'],
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
    document = controller.document

    schema = NoteSchema(exclude=('id', 'person_id', 'chrism_place', 'chrism_date',
                                 'marriage_district', 'marriage_date', 'spouse_name'))
    params = schema.load({
        'other_notes': request_json['other_notes']
    })

    controller = NoteController(
        note=Note(
            id=document.id,
            person_id=document.person_id,
            other_notes=params['other_notes']
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
        'child': request_json['child'],
        'parents_canonically_married': request_json['parents_canonically_married']
    })

    controller = RegistryOfBaptismsController(
        baptism=RegistryOfBaptisms(
            id=document.id,
            person_id=document.person_id,
            best_man=params['best_man']['id'],
            name=params['name'],
            surname=params['surname'],
            birth_date=params['birth_date'],
            birth_place=params['birth_place']['id'],
            identity_number=params['identity_number'],
            child=params['child']['id'],
            parents_canonically_married=params['parents_canonically_married']['id']
        ))
    controller.create()

    return jsonify(
        data=RegistryOfBaptismsController.get_one_details(controller.baptism.id),
        status=Status.status_successfully_inserted().__dict__)


@bpp.route('/registry_of_baptism/<string:baptism_id>', methods=['GET'])
@jwt_required
#@allow_access
def get_one_baptism(baptism_id):
    controller = RegistryOfBaptismsController.get_one_details(baptism_id)

    if controller is None:
        raise FlaskProjectLogException(Status.status_baptism_not_exist())

    return jsonify(
        data=controller,
        status=Status.status_successfully_processed().__dict__)






