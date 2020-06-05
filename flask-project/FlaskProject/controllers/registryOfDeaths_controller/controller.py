from sqlalchemy import and_
from ..persons_controller.controller import PersonController
from ..cities_controller.controller import CityController
from ..listItems_controller.controller import ListItemController
from ... import RegistryOfDeaths, Person, City, ListItem, FlaskProjectLogException, Document
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
    def __custom_sql(row_data):
        if row_data is not None:
            return_dict = obj_to_dict(row_data.RegistryOfDeaths)
            return_dict['person'] = obj_to_dict(row_data.Person)
            return_dict['place_of_death'] = obj_to_dict(row_data.City)
            return_dict['place_of_burial'] = obj_to_dict(row_data.ListItem)
            return return_dict
        return None



