from flask import request, jsonify
from ...flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity, get_jwt_claims
)
from .controller import RegistryOfDeathsController
from ..documents_controller.controller import DocumentController
from ..counter_controller.controller import CounterController
from ..persons_controller.controller import PersonController
from ..notes_controller.controller import NoteController
from ... import bpp, RegistryOfDeaths, FlaskProjectLogException, Document, Person, ListItem, Counter, Note
from ...general import Status, obj_to_dict
from ...general.route_decorators import allow_access
from ...schema import PersonSchema, RegistryOfDeathsSchema, NoteSchema, DocumentSchema


@bpp.route('/registry_of_death', methods=['POST'])
@jwt_required
#@allow_access
def create_registry_of_death():
    request_json = request.get_json()

    schema = DocumentSchema(exclude=('id', 'document_type', 'person2', 'document_number', 'user_created'))
    params = schema.load({
        'person': request_json['person'],
        'act_date': request_json['act_date'],
        'act_performed': request_json['act_performed'],
        'volume': request_json['volume'],
        'year': request_json['year'],
        'page': request_json['page'],
        'number': request_json['number'],
        'district': request_json['district']
    })

    current_user = get_jwt_claims()['id']
    document_type_value = ListItem.query.filter_by(value='Matica umrlih').first()

    controller = DocumentController(
        document=Document(
            document_type=document_type_value.id,
            person_id=params['person']['id'],
            act_date=params['act_date'],
            act_performed=params['act_performed']['id'],
            document_number='U - ' + CounterController.generate(Counter.counters['document_number']),
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
        'other_notes': request_json.get('other_notes', '')
    })

    controller = NoteController(
        note=Note(
            id=document.id,
            person_id=document.person_id,
            other_notes=params.get('other_notes', None)
        ))
    controller.create()

    schema = RegistryOfDeathsSchema(exclude=('id', 'person_id'))
    params = schema.load({
        'date_of_death': request_json['date_of_death'],
        'place_of_death': request_json['place_of_death'],
        'place_of_burial': request_json['place_of_burial']
    })

    controller = RegistryOfDeathsController(
        death=RegistryOfDeaths(
            id=document.id,
            person_id=document.person_id,
            date_of_death=params['date_of_death'],
            place_of_death=params['place_of_death']['id'],
            place_of_burial=params['place_of_burial']['id']
        ))
    controller.create()

    return jsonify(
        data=RegistryOfDeathsController.get_one_details(controller.death.id),
        status=Status.status_successfully_inserted().__dict__)


@bpp.route('/registry_of_deaths/<string:death_id>', methods=['GET'])
@jwt_required
#@allow_access
def get_one_death(death_id):
    controller = RegistryOfDeathsController.get_one_details(death_id)

    if controller is None:
        raise FlaskProjectLogException(Status.status_death_not_exist())

    return jsonify(
        data=controller,
        status=Status.status_successfully_processed().__dict__)
