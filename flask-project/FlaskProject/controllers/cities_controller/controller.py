from sqlalchemy import and_

from ..states_controller.controller import StateController
from ... import City, FlaskProjectLogException, State
from ...controllers.base_controller import BaseController
from ...general import Status, obj_to_dict


class CityController(BaseController):
    def __init__(self, city=City()):
        self.city = city

    def create(self):
        """
         Method used for creating city
        :return: Status object or raise FlaskProjectLogException
        """

        if City.query.check_if_already_exist_by_name(
                self.city.name):
            raise FlaskProjectLogException(
                Status.status_city_already_exist())

        if self.city.state_id is not None:
            state = StateController.get_one(
                self.city.state_id)

            if state.state is None:
                raise FlaskProjectLogException(
                    Status.status_state_not_exist())

        self.city.add()
        self.city.commit_or_rollback()

        return Status.status_successfully_inserted().__dict__

    def alter(self):
        """
         Method used for updating cities
         :return: Status object or raise FlaskProjectLogException
         """
        city = City.query.get_one(self.city.id)

        if city is None:
            raise FlaskProjectLogException(
                Status.status_city_not_exist())

        if City.query.check_if_name_is_taken(
                city.id, self.city.name):
            raise FlaskProjectLogException(
                Status.status_city_already_exist())

        if self.city.state_id is not None:
            state = StateController.get_one(
                self.city.state_id)

            if state.state is None:
                raise FlaskProjectLogException(
                    Status.status_state_not_exist())

        city.name = self.city.name
        city.state_id = self.city.state_id
        city.update()
        city.commit_or_rollback()

        self.city = city

        return Status.status_update_success().__dict__

    def inactivate(self):
        """
        Method used for setting cities status to inactive (0)
        :return: Status object or raise FlaskProjectLogException
        """
        city = City.query.get_one(self.city.id)

        if city is None:
            raise FlaskProjectLogException(
                Status.status_city_not_exist())

        city.status = City.STATUSES['inactive']

        city.update()
        city.commit_or_rollback()

        self.city = city

        return Status.status_successfully_processed().__dict__

    def activate(self):
        """
         Method used for setting cities status to active (1)
         :return: Status object or raise FlaskProjectLogException
         """
        city = City.query.get_one(self.city.id)

        if city is None:
            raise FlaskProjectLogException(
                Status.status_city_not_exist())

        city.status = City.STATUSES['active']

        city.update()
        city.commit_or_rollback()

        self.city = city

        return Status.status_successfully_processed().__dict__

    @classmethod
    def get_one(cls, identifier):
        return cls(city=City.query.get_one(identifier))

    @staticmethod
    def get_one_details(identifier):
        """
       Use this method to get a city film by identifier
       :param identifier: City film identifier
       :return: Dict object
       """
        return CityController.__custom_sql(
            City.query.get_one_details(identifier))

    @staticmethod
    def list_autocomplete(search):
        """
        Method for searching cities with autocomplete
        :param search:Data for search
        :return: List of dicts
        """
        list_data = []
        if search:
            state = City.query.autocomplete_by_name(search)
            for i in state:
                list_data.append(CityController.__custom_sql(i))

        return list_data

    @staticmethod
    def get_list_pagination(start, limit, **kwargs):
        """
        Method for getting all cities by filter_data in pagination form
        :return: dict with total, data and status
        """

        filter_main = and_()

        city_name = kwargs.get('city_name', None)
        state_id = kwargs.get('state_id', None)

        if city_name:
            filter_main = and_(
                filter_main, City.name.ilike('%' + city_name + '%'))

        if state_id:
            filter_main = and_(
                filter_main, State.id == state_id)

        data = City.query.get_all_by_filter(filter_main).paginate(
            page=start, error_out=False, per_page=limit)

        total = data.total
        list_data = []

        for i in data.items:
            list_data.append(CityController.__custom_sql(i))

        return dict(
            status=Status.status_successfully_processed().__dict__,
            total=total, data=list_data)

    @staticmethod
    def __custom_sql(row_data):
        if row_data is not None:
            return_dict = obj_to_dict(row_data.City)
            return_dict['state'] = obj_to_dict(row_data.State)
            return return_dict
        return None
