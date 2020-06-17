from sqlalchemy import and_
from ..persons_controller.controller import PersonController
from ... import Person, City, FlaskProjectLogException, District, Document, RegistryOfMarriages, Archdiocese, RegistryOfBaptisms, ListItem, User, Note, PersonExtraInfo
from ...controllers.base_controller import BaseController
from ...general import Status, obj_to_dict
from sqlalchemy.orm import relationship, foreign, aliased


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
            return_dict = obj_to_dict(row_data.RegistryOfMarriages)
            person2 = Person.query.filter_by(id=row_data.RegistryOfMarriages.person2_id).first()
            person1_birth_place = City.query.filter_by(id=row_data.Person.birth_place).first()
            person2_birth_place = City.query.filter_by(id=person2.birth_place).first()
            person1_mother = Person.query.filter_by(id=row_data.Person.mother_id).first()
            person1_father = Person.query.filter_by(id=row_data.Person.father_id).first()
            person2_mother = Person.query.filter_by(id=person2.mother_id).first()
            person2_father = Person.query.filter_by(id=person2.father_id).first()
            best_man1 = Person.query.filter_by(id=row_data.RegistryOfMarriages.best_man).first()
            best_man2 = Person.query.filter_by(id=row_data.RegistryOfMarriages.best_man2).first()
            document_marriage = Document.query.filter_by(id=row_data.RegistryOfMarriages.id).first()
            marriage_district = District.query.filter_by(id=document_marriage.district).first()
            marriage_archdiocese = Archdiocese.query.filter_by(id=marriage_district.archdiocese_id).first()
            person1_baptism_document = Document.query.filter_by(person_id=row_data.Person.id).filter(Document.document_number.ilike('%K%')).first()
            person1_extra_info = PersonExtraInfo.query.filter_by(person_id=row_data.Person.id).first()
            if person1_baptism_document is not None:
                person1_baptism_district = District.query.filter_by(id=person1_baptism_document.district).first()
            elif person1_extra_info is not None:
                person1_baptism_district = District.query.filter_by(id=person1_extra_info.baptism_district).first()
            else:
                person1_baptism_district = None
            person2_baptism_document = Document.query.filter_by(person_id=person2.id).filter(Document.document_number.ilike('%K%')).first()
            person2_extra_info = PersonExtraInfo.query.filter_by(person_id=person2.id).first()
            if person2_baptism_document is not None:
                person2_baptism_district = District.query.filter_by(id=person2_baptism_document.district).first()
            elif person2_extra_info is not None:
                person2_baptism_district = District.query.filter_by(id=person2_extra_info.baptism_district).first()
            else:
                person2_baptism_district = None
            person1_religion = ListItem.query.filter_by(id=Person.religion).first()
            person2_religion = ListItem.query.filter_by(id=person2.religion).first()
            person1_baptism = RegistryOfBaptisms.query.filter_by(person_id=row_data.Person.id).first()
            if person1_baptism is not None:
                person1_parents_canonically_married = ListItem.query.filter_by(id=person1_baptism.parents_canonically_married).first()
            elif person1_extra_info is not None:
                person1_parents_canonically_married = ListItem.query.filter_by(id=person1_extra_info.parents_canonically_married).first()
            else:
                person1_parents_canonically_married = None
            person2_baptism = RegistryOfBaptisms.query.filter_by(person_id=person2.id).first()
            if person2_baptism is not None:
                person2_parents_canonically_married = ListItem.query.filter_by(id=person2_baptism.parents_canonically_married).first()
            elif person2_extra_info is not None:
                person2_parents_canonically_married = ListItem.query.filter_by(id=person2_extra_info.parents_canonically_married).first()
            else:
                person2_parents_canonically_married = None
            return_dict['person1'] = obj_to_dict(row_data.Person)
            return_dict['person2'] = obj_to_dict(person2)
            return_dict['person1_birth_place'] = obj_to_dict(person1_birth_place)
            return_dict['person2_birth_place'] = obj_to_dict(person2_birth_place)
            return_dict['person1_mother'] = obj_to_dict(person1_mother)
            return_dict['person1_father'] = obj_to_dict(person1_father)
            return_dict['person2_mother'] = obj_to_dict(person2_mother)
            return_dict['person2_father'] = obj_to_dict(person2_father)
            return_dict['best_man1'] = obj_to_dict(best_man1)
            return_dict['best_man2'] = obj_to_dict(best_man2)
            return_dict['document_marriage'] = obj_to_dict(document_marriage)
            return_dict['marriage_district'] = obj_to_dict(marriage_district)
            return_dict['marriage_archdiocese'] = obj_to_dict(marriage_archdiocese)
            return_dict['person1_baptism_document'] = obj_to_dict(person1_baptism_document)
            return_dict['person1_baptism_district'] = obj_to_dict(person1_baptism_district)
            return_dict['person2_baptism_document'] = obj_to_dict(person2_baptism_document)
            return_dict['person2_baptism_district'] = obj_to_dict(person2_baptism_district)
            return_dict['person1_religion'] = obj_to_dict(person1_religion)
            return_dict['person2_religion'] = obj_to_dict(person2_religion)
            return_dict['person1_parents_canonically_married'] = obj_to_dict(person1_parents_canonically_married)
            return_dict['person2_parents_canonically_married'] = obj_to_dict(person2_parents_canonically_married)
            return_dict['act_performed'] = obj_to_dict(row_data.User)
            return_dict['note'] = obj_to_dict(row_data.Note)
            return return_dict
        return None



