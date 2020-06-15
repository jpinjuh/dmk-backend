from sqlalchemy import and_
from ..persons_controller.controller import PersonController
from ... import Person, City, FlaskProjectLogException, District, ChrismNote
from ...controllers.base_controller import BaseController
from ...general import Status, obj_to_dict


class ChrismNoteController(BaseController):
    def __init__(self, chrism=ChrismNote()):
        self.chrism = chrism

    def create(self):
        """
         Method used for creating registry of death
        :return: Status object or raise FlaskProjectLogException
        """
        if ChrismNote.query.check_if_already_exist(
                self.chrism.person_id):
            raise FlaskProjectLogException(
                Status.status_identity_number_already_exist())

        if self.chrism.person_id is not None:
            person = PersonController.get_one(
                self.chrism.person_id)

            if person.person is None:
                raise FlaskProjectLogException(
                    Status.status_person_not_exist())

        if self.chrism.best_man is not None:
            person = PersonController.get_one(
                self.chrism.best_man)

            if person.person is None:
                raise FlaskProjectLogException(
                    Status.status_person_not_exist())

        self.chrism.add()
        self.chrism.commit_or_rollback()

        return Status.status_successfully_inserted().__dict__

    def alter(self):
        raise NotImplementedError("To be implemented")

    def inactivate(self):
        raise NotImplementedError("To be implemented")

    def activate(self):
        raise NotImplementedError("To be implemented")

    @classmethod
    def get_one(cls, identifier):
        return cls(chrism=ChrismNote.query.get_one(identifier))

    @staticmethod
    def get_one_details(identifier):
        """
       Use this method to get an chrism note by identifier
       :param identifier: Chrism note identifier
       :return: Dict object
       """
        return ChrismNoteController.__custom_sql(
            ChrismNote.query.get_one_details(identifier))

    @staticmethod
    def list_autocomplete(search):
        raise NotImplementedError("To be implemented")

    @staticmethod
    def list_search(search):
        raise NotImplementedError("To be implemented")

    @staticmethod
    def get_list_pagination(start, limit, **kwargs):
        """
        Method for getting all registry of death by filter_data in pagination form
        :return: dict with total, data and status
        """
        raise NotImplementedError("To be implemented")

    @staticmethod
    def __custom_sql(row_data):
        if row_data is not None:
            return_dict = obj_to_dict(row_data.RegistryOfDeaths)
            person = Person.query.filter_by(id=row_data.RegistryOfDeaths.person_id).first()
            mother = Person.query.filter_by(id=person.mother_id).first()
            father = Person.query.filter_by(id=person.father_id).first()
            birth = City.query.filter_by(id=row_data.RegistryOfBaptisms.birth_place).first()
            district_person = District.query.filter_by(id=row_data.Person.district).first()
            district_baptism = District.query.filter_by(id=row_data.Document.district).first()
            return_dict['person'] = obj_to_dict(person)
            return_dict['mother'] = obj_to_dict(mother)
            return_dict['father'] = obj_to_dict(father)
            return_dict['district_person'] = obj_to_dict(district_person)
            return_dict['district_baptism'] = obj_to_dict(district_baptism)
            return_dict['archdiocese'] = obj_to_dict(row_data.Archdiocese)
            return_dict['act_performed'] = obj_to_dict(row_data.User)
            return_dict['document'] = obj_to_dict(row_data.Document)
            return_dict['birth_place'] = obj_to_dict(birth)
            return_dict['note'] = obj_to_dict(row_data.Note)
            return return_dict
        return None



