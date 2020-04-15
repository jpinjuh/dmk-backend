from sqlalchemy import and_

from ..districts_controller.controller import DistrictController
from ..roles_controller.controller import RoleController
from ... import User, FlaskProjectLogException, Role, District
from ...controllers.base_controller import BaseController
from ...general import Status, obj_to_dict
from werkzeug.security import generate_password_hash, check_password_hash


class UserController(BaseController):
    def __init__(self, user=User()):
        self.user = user

    def create(self):
        """
         Method used for creating user
        :return: Status object or raise FlaskProjectLogException
        """
        if User.query.check_if_already_exist_by_name(
                self.user.username):
            raise FlaskProjectLogException(
                Status.status_user_already_exist())

        if User.query.check_if_already_exist_by_email(
                self.user.email):
            raise FlaskProjectLogException(
                Status.status_user_already_exist())

        if self.user.roles_id is not None:
            user_role = RoleController.get_one(
                self.user.roles_id)

            if user_role.role is None:
                raise FlaskProjectLogException(
                    Status.status_role_not_exist())

        if self.user.districts_id is not None:
            district_role = DistrictController.get_one(
                self.user.districts_id)

            if district_role.district is None:
                raise FlaskProjectLogException(
                    Status.status_district_not_exist())

        self.user.add()
        self.user.commit_or_rollback()

        return Status.status_successfully_inserted().__dict__



    def alter(self):
        raise NotImplementedError("To be implemented")

    def inactivate(self):
        raise NotImplementedError("To be implemented")

    def activate(self):
        raise NotImplementedError("To be implemented")

    @classmethod
    def get_one(cls, identifier):
        return cls(user=User.query.get_one(identifier))

    @staticmethod
    def get_one_details(identifier):
        """
       Use this method to get an user by identifier
       :param identifier: User identifier
       :return: Dict object
       """
        return UserController.__custom_sql(
            User.query.get_one_details(identifier))

    @staticmethod
    def list_autocomplete(search):
        """
        Method for searching users with autocomplete
        :param search:Data for search
        :return: List of dicts
        """
        list_data = []
        if search:
            role_district = User.query.autocomplete_by_name(search)
            for i in role_district:
                list_data.append(UserController.__custom_sql(i))

        return list_data

    @staticmethod
    def get_list_pagination(start, limit, **kwargs):
        """
        Method for getting all users by filter_data in pagination form
        :return: dict with total, data and status
        """

        filter_main = and_()

        first_name = kwargs.get('first_name', None)
        last_name = kwargs.get('last_name', None)
        username = kwargs.get('username', None)
        email = kwargs.get('email', None)
        roles_id = kwargs.get('roles_id', None)
        districts_id = kwargs.get('districts_id', None)

        if first_name:
            filter_main = and_(
                filter_main, User.first_name.ilike('%' + first_name + '%'))

        if last_name:
            filter_main = and_(
                filter_main, User.last_name.ilike('%' + last_name + '%'))

        if username:
            filter_main = and_(
                filter_main, User.username.ilike('%' + username + '%'))

        if email:
            filter_main = and_(
                filter_main, User.email.ilike('%' + email + '%'))

        if roles_id:
            filter_main = and_(
                filter_main, Role.id == roles_id)

        if districts_id:
            filter_main = and_(
                filter_main, District.id == districts_id)

        data = User.query.get_all_by_filter(filter_main).paginate(
            page=start, error_out=False, per_page=limit)

        total = data.total
        list_data = []

        for i in data.items:
            list_data.append(UserController.__custom_sql(i))

        return dict(
            status=Status.status_successfully_processed().__dict__,
            total=total, data=list_data)

    @staticmethod
    def __custom_sql(row_data):
        if row_data is not None:
            return_dict = obj_to_dict(row_data.User)
            return_dict['role'] = obj_to_dict(row_data.Role)
            return_dict['district'] = obj_to_dict(row_data.District)
            return return_dict
        return None