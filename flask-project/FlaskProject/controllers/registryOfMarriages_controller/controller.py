from sqlalchemy import and_
from ..persons_controller.controller import PersonController
from ... import Person, City, FlaskProjectLogException, District, Document, RegistryOfMarriages
from ...controllers.base_controller import BaseController
from ...general import Status, obj_to_dict


class RegistryOfMarriagesController(BaseController):
    def __init__(self, marriage=RegistryOfMarriages()):
        self.marriage = marriage

    def create(self):
        """
         Method used for creating registry of marriage
        :return: Status object or raise FlaskProjectLogException
        """

        if self.marriage.person_id is not None:
            person = PersonController.get_one(
                self.marriage.person_id)

            if person.person is None:
                raise FlaskProjectLogException(
                    Status.status_person_not_exist())

        if self.marriage.person2_id is not None:
            person = PersonController.get_one(
                self.marriage.person2_id)

            if person.person is None:
                raise FlaskProjectLogException(
                    Status.status_person_not_exist())

        if self.marriage.best_man is not None:
            person = PersonController.get_one(
                self.marriage.best_man)

            if person.person is None:
                raise FlaskProjectLogException(
                    Status.status_person_not_exist())

        if self.marriage.best_man2 is not None:
            person = PersonController.get_one(
                self.marriage.best_man2)

            if person.person is None:
                raise FlaskProjectLogException(
                    Status.status_person_not_exist())

        self.marriage.add()
        self.marriage.commit_or_rollback()

        return Status.status_successfully_inserted().__dict__

    def alter(self):
        raise NotImplementedError("To be implemented")

    def inactivate(self):
        raise NotImplementedError("To be implemented")

    def activate(self):
        raise NotImplementedError("To be implemented")

    @classmethod
    def get_one(cls, identifier):
        return cls(marriage=RegistryOfMarriages.query.get_one(identifier))

    @staticmethod
    def get_one_details(identifier):
        """
       Use this method to get a registry of marriage by identifier
       :param identifier: Chrism note identifier
       :return: Dict object
       """
        return RegistryOfMarriagesController.__custom_sql(
            RegistryOfMarriages.query.get_one_details(identifier))

    @staticmethod
    def list_autocomplete(search):
        raise NotImplementedError("To be implemented")

    @staticmethod
    def list_search(search):
        raise NotImplementedError("To be implemented")

    @staticmethod
    def get_list_pagination(start, limit, **kwargs):
        """
        Method for getting all registry of marriages by filter_data in pagination form
        :return: dict with total, data and status
        """
        raise NotImplementedError("To be implemented")

    @staticmethod
    def __custom_sql(row_data):
        if row_data is not None:
            return_dict = obj_to_dict(row_data.ChrismNote)
            person = Person.query.filter_by(id=row_data.ChrismNote.person_id).first()
            mother = Person.query.filter_by(id=person.mother_id).first()
            father = Person.query.filter_by(id=person.father_id).first()
            best_man = Person.query.filter_by(id=row_data.ChrismNote.best_man).first()
            birth_place = City.query.filter_by(id=person.birth_place).first()
            document_baptism = Document.query.filter_by(person_id=row_data.ChrismNote.person_id).filter(Document.document_number.ilike('%K%')).first()
            baptism_district = District.query.filter_by(id=document_baptism.district).first()
            return_dict['person'] = obj_to_dict(person)
            return_dict['birth_place'] = obj_to_dict(birth_place)
            return_dict['mother'] = obj_to_dict(mother)
            return_dict['father'] = obj_to_dict(father)
            return_dict['best_man'] = obj_to_dict(best_man)
            return_dict['document_baptism'] = obj_to_dict(document_baptism)
            return_dict['baptism_district'] = obj_to_dict(baptism_district)
            return_dict['act_performed'] = obj_to_dict(row_data.User)
            return return_dict
        return None



