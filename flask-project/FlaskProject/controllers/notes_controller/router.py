from flask import request, jsonify
from ...flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity, get_jwt_claims
)
from .controller import NoteController
from ... import bpp, Note, FlaskProjectLogException
from ...general import Status, obj_to_dict
from ...general.route_decorators import allow_access
from ...schema import NoteSchema


@bpp.route('/note/<string:note_id>', methods=['PUT'])
@jwt_required
#@allow_access
def alter_note(note_id):
    request_json = request.get_json()
    schema = NoteSchema(exclude=('id', 'person_id', 'chrism_place', 'chrism_date', 'marriage_district',
                                 'marriage_date', 'spouse_name'))

    params = schema.load(request_json)

    note = Note.query.filter_by(id=note_id).first()

    controller = NoteController(
        note=Note(
            id=note_id,
            person_id=note.person_id,
            chrism_place=note.chrism_place,
            chrism_date=note.chrism_date,
            marriage_district=note.marriage_district,
            marriage_date=note.marriage_date,
            spouse_name=note.spouse_name,
            other_notes=params.get('other_notes', None)
        ))
    controller.alter()

    return jsonify(
        data=NoteController.get_one_details(controller.note.id),
        status=Status.status_update_success().__dict__)
