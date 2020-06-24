from ..persons_controller.controller import PersonController
from ..cities_controller.controller import CityController
from ..listItems_controller.controller import ListItemController
from ... import RegistryOfDeaths, Person, City, ListItem, FlaskProjectLogException, District, RegistryOfBaptisms, RegistryOfMarriages
from ...controllers.base_controller import BaseController
from ...general import Status, obj_to_dict


class RegistryOfDeathsController(BaseController):
    def __init__(self, death=RegistryOfDeaths()):
        self.death = death

    def create(self):
        """
         Method used for creating registry of death
        :return: Status object or raise FlaskProjectLogException
        """
        if RegistryOfDeaths.query.check_if_already_exist(
                self.death.person_id):
            raise FlaskProjectLogException(
                Status.status_identity_number_already_exist())

        if self.death.person_id is not None:
            person = PersonController.get_one(
                self.death.person_id)

            if person.person is None:
                raise FlaskProjectLogException(
                    Status.status_person_not_exist())

        if self.death.place_of_death is not None:
            place_of_death = CityController.get_one(
                self.death.place_of_death)

            if place_of_death.city is None:
                raise FlaskProjectLogException(
                    Status.status_city_not_exist())

        if self.death.place_of_burial is not None:
            place_of_burial = ListItemController.get_one(
                self.death.place_of_burial)

            if place_of_burial.list_item is None:
                raise FlaskProjectLogException(
                    Status.status_list_item_not_exist())

        self.death.add()
        self.death.commit_or_rollback()

        return Status.status_successfully_inserted().__dict__

    def alter(self):
        raise NotImplementedError("To be implemented")

    def inactivate(self):
        raise NotImplementedError("To be implemented")

    def activate(self):
        raise NotImplementedError("To be implemented")

    @classmethod
    def get_one(cls, identifier):
        return cls(death=RegistryOfDeaths.query.get_one(identifier))

    @staticmethod
    def get_one_details(identifier):
        """
       Use this method to get an registry of death by identifier
       :param identifier: Registry of death identifier
       :return: Dict object
       """
        return RegistryOfDeathsController.__custom_sql(
            RegistryOfDeaths.query.get_one_details(identifier))

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
    def get_spouses(person_id):
        spouse_list=[]
        if person_id:
            document_marriage1 = RegistryOfMarriages.query.filter_by(person_id=person_id).all()
            if document_marriage1 is not None:
                for i in document_marriage1:
                    spouse = Person.query.filter_by(id=i.person2_id).first()
                    spouse_name = {
                        'first_name': spouse.first_name,
                        'last_name': spouse.last_name
                    }
                    spouse_list.append(spouse_name)

            document_marriage2 = RegistryOfMarriages.query.filter_by(person2_id=person_id).all()
            if document_marriage2 is not None:
                for i in document_marriage2:
                    spouse = Person.query.filter_by(id=i.person_id).first()
                    spouse_name = {
                        'first_name': spouse.first_name,
                        'last_name': spouse.last_name
                    }
                    spouse_list.append(spouse_name)

        return spouse_list

    @staticmethod
    def __custom_sql(row_data):
        if row_data is not None:
            return_dict = obj_to_dict(row_data.RegistryOfDeaths)
            person = Person.query.filter_by(id=row_data.RegistryOfDeaths.person_id).first()
            mother = Person.query.filter_by(id=person.mother_id).first()
            father = Person.query.filter_by(id=person.father_id).first()
            death = City.query.filter_by(id=row_data.RegistryOfDeaths.place_of_death).first()
            birth = City.query.filter_by(id=row_data.RegistryOfBaptisms.birth_place).first()
            district_person = District.query.filter_by(id=row_data.Person.district).first()
            district_baptism = District.query.filter_by(id=row_data.Document.district).first()
            registry_of_baptism = RegistryOfBaptisms.query.filter_by(person_id=person.id).first()
            gender = ListItem.query.filter_by(id=registry_of_baptism.child).first() if registry_of_baptism is not None else None
            return_dict['person'] = obj_to_dict(person)
            return_dict['place_of_death'] = obj_to_dict(death)
            return_dict['place_of_burial'] = obj_to_dict(row_data.ListItem)
            return_dict['mother'] = obj_to_dict(mother)
            return_dict['father'] = obj_to_dict(father)
            return_dict['district_person'] = obj_to_dict(district_person)
            return_dict['district_baptism'] = obj_to_dict(district_baptism)
            return_dict['archdiocese'] = obj_to_dict(row_data.Archdiocese)
            return_dict['gender'] = obj_to_dict(gender)
            return_dict['act_performed'] = obj_to_dict(row_data.User)
            return_dict['document'] = obj_to_dict(row_data.Document)
            return_dict['birth_place'] = obj_to_dict(birth)
            return_dict['note'] = obj_to_dict(row_data.Note)
            return_dict['spouses'] = RegistryOfDeathsController.get_spouses(row_data.RegistryOfDeaths.person_id)
            return_dict['sacraments'] = PersonController.get_person_sacraments(row_data.RegistryOfDeaths.person_id)
            return return_dict
        return None



