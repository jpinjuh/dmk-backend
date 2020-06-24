from flask import request, jsonify
from ...flask_jwt_extended import (
    jwt_required, get_jwt_claims
)
from .controller import ChrismNoteController
from ..documents_controller.controller import DocumentController
from ..counter_controller.controller import CounterController
from ..notes_controller.controller import NoteController
from ... import bpp, FlaskProjectLogException,\
    Document, ListItem, Counter, ChrismNote, Note, City, District, RegistryOfBaptisms
from ...general import Status
from ...general.route_decorators import allow_access
from ...schema import ChrismNoteSchema, DocumentSchema


@bpp.route('/chrism_note', methods=['POST'])
@jwt_required
#@allow_access
def create_chrism_note():
    request_json = request.get_json()

    schema = DocumentSchema(exclude=('id', 'document_type', 'person2', 'document_number', 'user_created', 'volume', 'year', 'page', 'number'))
    params = schema.load({
        'person': request_json['person'],
        'act_date': request_json['act_date'],
        'act_performed': request_json['act_performed'],
        'district': request_json['district']
    })

    current_user = get_jwt_claims()['id']
    document_type_value = ListItem.query.filter_by(value='Matica krizmanih').first()

    controller = DocumentController(
        document=Document(
            person_id=params['person']['id'],
            document_type=document_type_value.id,
            act_date=params['act_date'],
            act_performed=params['act_performed']['id'],
            document_number='P - ' + CounterController.generate(Counter.counters['document_number']),
            district=params['district']['id'],
            user_created=current_user
        ))
    controller.create()

    document = controller.document

    district = District.query.filter_by(id=document.district).first()
    city = City.query.filter_by(id=district.city_id).first()
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
                chrism_place=city.id,
                chrism_date=document.act_date,
                marriage_district=baptism_note.marriage_district,
                marriage_date=baptism_note.marriage_date,
                spouse_name=baptism_note.spouse_name
            ))
        controller.alter()
    if baptism_document is not None and baptism_note is None:
        controller = NoteController(
            note=Note(
                id=baptism_document.id,
                person_id=document.person_id,
                chrism_place=city.id,
                chrism_date=document.act_date
            ))
        controller.create()
    schema = ChrismNoteSchema(exclude=('id',))
    params = schema.load({
        'person': request_json['person'],
        'best_man': request_json['best_man'],
    })

    controller = ChrismNoteController(
        chrism=ChrismNote(
            id=document.id,
            person_id=params['person']['id'],
            best_man=params['best_man']['id'],
        ))
    controller.create()

    return jsonify(
        data=ChrismNoteController.get_one_details(controller.chrism.id),
        status=Status.status_successfully_inserted().__dict__)


@bpp.route('/chrism_note/<string:chrism_id>', methods=['GET'])
@jwt_required
#@allow_access
def get_one_chrism(chrism_id):
    controller = ChrismNoteController.get_one_details(chrism_id)

    if controller is None:
        raise FlaskProjectLogException(Status.status_chrism_not_exist())

    return jsonify(
        data=controller,
        status=Status.status_successfully_processed().__dict__)


