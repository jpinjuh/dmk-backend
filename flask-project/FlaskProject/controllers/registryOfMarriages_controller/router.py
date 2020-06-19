from flask import request, jsonify
from ...flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity, get_jwt_claims
)
from .controller import RegistryOfMarriagesController
from ..documents_controller.controller import DocumentController
from ..counter_controller.controller import CounterController
from ..persons_controller.controller import PersonController
from ..notes_controller.controller import NoteController
from ... import bpp, RegistryOfMarriages, FlaskProjectLogException, Document, Person, ListItem, Counter, Note, District, RegistryOfBaptisms
from ...general import Status, obj_to_dict
from ...general.route_decorators import allow_access
from ...schema import PersonSchema, NoteSchema, DocumentSchema, RegistryOfMarriagesSchema


@bpp.route('/registry_of_marriage', methods=['POST'])
@jwt_required
#@allow_access
def create_registry_of_marriage():
    request_json = request.get_json()

    schema = DocumentSchema(exclude=('id', 'document_type', 'document_number', 'user_created'))
    params = schema.load({
        'person': request_json['person'],
        'person2': request_json['person2'],
        'act_date': request_json['act_date'],
        'act_performed': request_json['act_performed'],
        'volume': request_json['volume'],
        'year': request_json['year'],
        'page': request_json['page'],
        'number': request_json['number'],
        'district': request_json['district']
    })

    current_user = get_jwt_claims()['id']
    document_type_value = ListItem.query.filter_by(value='Matica vjenčanih').first()

    controller = DocumentController(
        document=Document(
            document_type=document_type_value.id,
            person_id=params['person']['id'],
            person2_id=params['person2']['id'],
            act_date=params['act_date'],
            act_performed=params['act_performed']['id'],
            document_number='V - ' + CounterController.generate(Counter.counters['document_number']),
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

    district_marriage = District.query.filter_by(id=document.district).first()
    spouse = Person.query.filter_by(id=document.person2_id).first()
    baptism_document = RegistryOfBaptisms.query.filter_by(person_id=document.person_id).first()
    if baptism_document is not None:
        baptism_note = Note.query.filter_by(id=baptism_document.id).first()
    else:
        baptism_note = None
    if baptism_document is not None and baptism_note is not None:
        controller = NoteController(
            note=Note(
                id=baptism_document.id,
                person_id=document.person_id,
                marriage_district=district_marriage.id,
                marriage_date=document.act_date,
                spouse_name=spouse.first_name,
                chrism_place=baptism_note.chrism_place,
                chrism_date=baptism_note.chrism_date
            ))
        controller.alter()
    if baptism_document is not None and baptism_note is None:
        controller = NoteController(
            note=Note(
                id=baptism_document.id,
                person_id=document.person_id,
                marriage_district=district_marriage.id,
                marriage_date=document.act_date,
                spouse_name=spouse.first_name
            ))
        controller.create()

    spouse = Person.query.filter_by(id=document.person_id).first()
    baptism_document = RegistryOfBaptisms.query.filter_by(person_id=document.person2_id).first()
    if baptism_document is not None:
        baptism_note = Note.query.filter_by(id=baptism_document.id).first()
    else:
        baptism_note = None
    if baptism_document is not None and baptism_note is not None:
        controller = NoteController(
            note=Note(
                id=baptism_document.id,
                person_id=document.person2_id,
                marriage_district=district_marriage.id,
                marriage_date=document.act_date,
                spouse_name=spouse.first_name,
                chrism_place=baptism_note.chrism_place,
                chrism_date=baptism_note.chrism_date
            ))
        controller.alter()
    if baptism_document is not None and baptism_note is None:
        controller = NoteController(
            note=Note(
                id=baptism_document.id,
                person_id=document.person2_id,
                marriage_district=district_marriage.id,
                marriage_date=document.act_date,
                spouse_name=spouse.first_name
            ))
        controller.create()

    schema = RegistryOfMarriagesSchema(exclude=('id', 'person_id', 'person2_id'))
    params = schema.load({
        'best_man': request_json['best_man'],
        'best_man2': request_json['best_man2']
    })

    controller = RegistryOfMarriagesController(
        marriage=RegistryOfMarriages(
            id=document.id,
            person_id=document.person_id,
            person2_id=document.person2_id,
            best_man=params['best_man']['id'],
            best_man2=params['best_man2']['id']
        ))
    controller.create()

    return jsonify(
        data=RegistryOfMarriagesController.get_one_details(controller.marriage.id),
        status=Status.status_successfully_inserted().__dict__)


@bpp.route('/registry_of_marriages/<string:marriage_id>', methods=['GET'])
@jwt_required
#@allow_access
def get_one_marriage(marriage_id):
    controller = RegistryOfMarriagesController.get_one_details(marriage_id)

    if controller is None:
        raise FlaskProjectLogException(Status.status_marriage_not_exist())

    return jsonify(
        data=controller,
        status=Status.status_successfully_processed().__dict__)



