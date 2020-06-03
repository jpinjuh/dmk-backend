from sqlalchemy import and_

from ... import Note, FlaskProjectLogException
from ...controllers.base_controller import BaseController
from ...general import Status, obj_to_dict

class NoteController(BaseController):

    def __init__(self, note=Note()):
        self.note = note

    def create(self):
        """
        Method used for creating note
        :return: Status object or raise FlaskProjectLogException
        """

        self.note.add()
        self.note.commit_or_rollback()

        return Status.status_successfully_inserted().__dict__

    def alter(self):
        """
        Method used for updating notes
        :return: Status object or raise FlaskProjectLogException
        """
        note = Note.query.get_one(self.note.id)

        if note is None:
            raise FlaskProjectLogException(
                Status.status_note_not_exist())

        note.person_id = self.note.person_id
        note.chrism_place = self.note.chrism_place
        note.chrism_date = self.note.chrism_date
        note.marriage_district = self.note.marriage_district
        note.marriage_date = self.note.marriage_date
        note.spouse_name = self.note.spouse_name
        note.other_notes = self.note.other_notes
        note.update()
        note.commit_or_rollback()

        self.note = note

        return Status.status_update_success().__dict__

    def inactivate(self):
        raise NotImplementedError("To be implemented")

    def activate(self):
        raise NotImplementedError("To be implemented")

    @classmethod
    def get_one(cls, identifier):
        """
        Use this method to get a note by identifier
        :param identifier: Extras State identifier
        :return: NoteController object
        """

        return cls(note=Note.query.get_one(identifier))

    @staticmethod
    def get_one_details(identifier):
        """
        Use this method to get a note film by identifier
       :param identifier: Note identifier
       :return: Dict object
       """
        return NoteController.__custom_sql(
            Note.query.get_one_details(identifier))

    @staticmethod
    def list_autocomplete(search):
        raise NotImplementedError("To be implemented")

    @staticmethod
    def get_list_pagination(start, limit, **kwargs):
        raise NotImplementedError("To be implemented")
