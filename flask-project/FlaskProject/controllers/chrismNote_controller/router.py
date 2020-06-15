from flask import request, jsonify
from ...flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity, get_jwt_claims
)
from .controller import ChrismNoteController
from ..documents_controller.controller import DocumentController
from ..counter_controller.controller import CounterController
from ..persons_controller.controller import PersonController
from ..notes_controller.controller import NoteController
from ... import bpp, RegistryOfDeaths, FlaskProjectLogException, Document, Person, ListItem, Counter, ChrismNote
from ...general import Status, obj_to_dict
from ...general.route_decorators import allow_access
from ...schema import PersonSchema, ChrismNoteSchema, NoteSchema, DocumentSchema


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
    document_type_value = ListItem.query.filter_by(value='Matica krštenih').first()

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


