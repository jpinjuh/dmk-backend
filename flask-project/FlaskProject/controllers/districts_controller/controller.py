from sqlalchemy import and_

from ..cities_controller.controller import CityController
from ... import City, FlaskProjectLogException, State, District
from ...controllers.base_controller import BaseController
from ...general import Status, obj_to_dict


class DistrictController(BaseController):
    def __init__(self, district=District()):
        self.district = district

    def create(self):
        """
         Method used for creating district
        :return: Status object or raise FlaskProjectLogException
        """
        if District.query.check_if_already_exist_by_name(
                self.district.name):
            raise FlaskProjectLogException(
                Status.status_district_already_exist())

        if District.query.check_if_already_exist_by_name(
                self.district.name):
            raise FlaskProjectLogException(
                Status.status_district_already_exist())

        if self.district.city_id is not None:
            city = CityController.get_one(
                self.district.city_id)

            if city.city is None:
                raise FlaskProjectLogException(
                    Status.status_city_not_exist())

        self.district.add()
        self.district.commit_or_rollback()

        return Status.status_successfully_inserted().__dict__

    def alter(self):
        """
         Method used for updating districts
         :return: Status object or raise FlaskProjectLogException
         """

        district = District.query.get_one(self.district.id)

        if district is None:
            raise FlaskProjectLogException(
                Status.status_district_not_exist())

        if District.query.check_if_name_is_taken(
                district.id, self.district.name):
            raise FlaskProjectLogException(
                Status.status_district_already_exist())

        if self.district.city_id is not None:
            city = CityController.get_one(
                self.district.city_id)

            if city.city is None:
                raise FlaskProjectLogException(
                    Status.status_city_not_exist())


        district.name = self.district.name
        district.city_id = self.district.city_id
        district.update()
        district.commit_or_rollback()

        self.district = district

        return Status.status_update_success().__dict__

    def inactivate(self):
        """
        Method used for setting districts status to inactive (0)
        :return: Status object or raise FlaskProjectLogException
        """

        district = District.query.get_one(self.district.id)

        if district is None:
            raise FlaskProjectLogException(
                Status.status_district_not_exist())

        district.status = District.STATUSES['inactive']

        district.update()
        district.commit_or_rollback()

        self.district = district

        return Status.status_successfully_processed().__dict__

    def activate(self):
        """
         Method used for setting districts status to active (1)
         :return: Status object or raise FlaskProjectLogException
         """

        district = District.query.get_one(self.district.id)

        if district is None:
            raise FlaskProjectLogException(
                Status.status_district_not_exist())

        district.status = District.STATUSES['active']

        district.update()
        district.commit_or_rollback()

        self.district = district

        return Status.status_successfully_processed().__dict__

    @classmethod
    def get_one(cls, identifier):
        return cls(district=District.query.get_one(identifier))

    @staticmethod
    def get_one_details(identifier):
        """
       Use this method to get a district by identifier
       :param identifier: District identifier
       :return: Dict object
       """
        return DistrictController.__custom_sql(
            District.query.get_one_details(identifier))

    @staticmethod
    def list_autocomplete(search):
        """
        Method for searching districts with autocomplete
        :param search:Data for search
        :return: List of dicts
        """
        list_data = []
        if search:
            city = District.query.autocomplete_by_name(search)
            for i in city:
                list_data.append(DistrictController.__custom_sql(i))

        return list_data

    @staticmethod
    def get_list_pagination(start, limit, **kwargs):
        """
        Method for getting all districts by filter_data in pagination form
        :return: dict with total, data and status
        """

        filter_main = and_()

        district_name = kwargs.get('district_name', None)
        city_id = kwargs.get('city_id', None)

        if district_name:
            filter_main = and_(
                filter_main, District.name.ilike('%' + district_name + '%'))

        if city_id:
            filter_main = and_(
                filter_main, City.id == city_id)

        data = District.query.get_all_by_filter(filter_main).paginate(
            page=start, error_out=False, per_page=limit)

        total = data.total
        list_data = []

        for i in data.items:
            list_data.append(DistrictController.__custom_sql(i))

        return dict(
            status=Status.status_successfully_processed().__dict__,
            total=total, data=list_data)

    @staticmethod
    def __custom_sql(row_data):
        if row_data is not None:
            return_dict = obj_to_dict(row_data.District)
            return_dict['city'] = obj_to_dict(row_data.City)
            return return_dict
        return None
