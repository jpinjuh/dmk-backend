from sqlalchemy import and_

from ..roles_controller.controller import RoleController
from ..permissions_controller.controller import PermissionController
from ... import Privilege, FlaskProjectLogException, Role, Permission
from ...controllers.base_controller import BaseController
from ...general import Status, obj_to_dict


class PrivilegeController(BaseController):
    def __init__(self, privilege=Privilege()):
        self.privilege = privilege

    def create(self):
        """
         Method used for creating privilege
        :return: Status object or raise FlaskProjectLogException
        """
        if Privilege.query.check_if_already_exist(
               self.privilege.roles_id, self.privilege.permissions_id):
            raise FlaskProjectLogException(
                Status.status_privilege_already_exist())

        if self.privilege.roles_id is not None:
            role = RoleController.get_one(
                self.privilege.roles_id)

            if role.role is None:
                raise FlaskProjectLogException(
                    Status.status_role_not_exist())

        if self.privilege.permissions_id is not None:
            permission = PermissionController.get_one(
                self.privilege.permissions_id)

            if permission.permission is None:
                raise FlaskProjectLogException(
                    Status.status_permission_not_exist())

        self.privilege.add()
        self.privilege.commit_or_rollback()

        return Status.status_successfully_inserted().__dict__

    def alter(self):
        """
        Method used for updating privileges
        :return: Status object or raise FlaskProjectLogException
        """

        privilege = Privilege.query.get_one(self.privilege.id)

        if privilege is None:
            raise FlaskProjectLogException(
                Status.status_privilege_not_exist())

        if self.privilege.roles_id is not None:
            role = RoleController.get_one(
                self.privilege.roles_id)

            if role.role is None:
                raise FlaskProjectLogException(
                    Status.status_role_not_exist())

        if self.privilege.permissions_id is not None:
            permission = PermissionController.get_one(
                self.privilege.permissions_id)

            if permission.permission is None:
                raise FlaskProjectLogException(
                    Status.status_permission_not_exist())

        privilege.roles_id = self.privilege.roles_id
        privilege.permissions_id = self.privilege.permissions_id
        privilege.update()
        privilege.commit_or_rollback()

        self.privilege = privilege

        return Status.status_update_success().__dict__

    def inactivate(self):
        """
        Method used for setting privileges status to inactive (0)
        :return: Status object or raise FlaskProjectLogException
        """
        privilege = Privilege.query.get_one(self.privilege.id)

        if privilege is None:
            raise FlaskProjectLogException(
                Status.status_privilege_not_exist())

        privilege.status = Privilege.STATUSES['inactive']

        privilege.update()
        privilege.commit_or_rollback()

        self.privilege = privilege

        return Status.status_successfully_processed().__dict__

    def activate(self):
        """
        Method used for setting privileges status to active (1)
        :return: Status object or raise FlaskProjectLogException
        """
        privilege = Privilege.query.get_one(self.privilege.id)

        if privilege is None:
            raise FlaskProjectLogException(
                Status.status_privilege_not_exist())

        privilege.status = Privilege.STATUSES['active']

        privilege.update()
        privilege.commit_or_rollback()

        self.privilege = privilege

        return Status.status_successfully_processed().__dict__

    @classmethod
    def get_one(cls, identifier):
        return cls(privilege=Privilege.query.get_one(identifier))

    @staticmethod
    def get_one_details(identifier):
        """
       Use this method to get a privilege by identifier
       :param identifier: Privilege identifier
       :return: Dict object
       """
        return PrivilegeController.__custom_sql(
            Privilege.query.get_one_details(identifier))

    @staticmethod
    def list_autocomplete(search):
        """
        Method for searching privileges with autocomplete
        :param search:Data for search
        :return: List of dicts
        """
        list_data = []
        if search:
            role_permission = Privilege.query.autocomplete_by_name(search)
            for i in role_permission:
                list_data.append(PrivilegeController.__custom_sql(i))
        return list_data

    @staticmethod
    def list_search(search):
        """
        Method for searching privileges
        :param search: Data for search
        :return: List of dicts
        """
        list_data = []
        if search:
            role_permission = Privilege.query.autocomplete_by_name(search)
            for i in role_permission:
                list_data.append(PrivilegeController.__custom_sql(i))

        else:
            role_permission = Privilege.query.get_all()
            for i in role_permission:
                list_data.append(PrivilegeController.__custom_sql(i))

        return list_data

    @staticmethod
    def get_list_pagination(start, limit, **kwargs):
        """
        Method for getting all privileges by filter_data in pagination form
        :return: dict with total, data and status
        """

        filter_main = and_()

        privilege_name = kwargs.get('privilege_name', None)
        role_id = kwargs.get('role_id', None)
        permission_id = kwargs.get('role_id', None)

        if privilege_name:
            filter_main = and_(
                filter_main, Privilege.name.ilike('%' + city_name + '%'))

        if role_id:
            filter_main = and_(
                filter_main, Role.id == role_id)

        if permission_id:
            filter_main = and_(
                filter_main, Permission.id == permission_id)

        data = Privilege.query.get_all_by_filter(filter_main).paginate(
            page=start, error_out=False, per_page=limit)

        total = data.total
        list_data = []

        for i in data.items:
            list_data.append(PrivilegeController.__custom_sql(i))

        return dict(
            status=Status.status_successfully_processed().__dict__,
            total=total, data=list_data)

    @staticmethod
    def __custom_sql(row_data):
        if row_data is not None:
            return_dict = obj_to_dict(row_data.Privilege)
            return_dict['role'] = obj_to_dict(row_data.Role)
            return_dict['permission'] = obj_to_dict(row_data.Permission)
            return return_dict
        return None

    @staticmethod
    def get_role_permissions(role_id):

        list_method_route = []

        if role_id:
            filter_main = and_()
            if role_id:
                filter_main = and_(
                    filter_main, Privilege.roles_id == role_id)

            privileges = Privilege.query.get_all_by_filter(filter_main).filter(Privilege.status == Privilege.STATUSES['active'])
            list_role_permissions = []
            for i in privileges:
                list_role_permissions.append(PrivilegeController.__custom_sql(i))

            for i in list_role_permissions:
                method_role = {
                    'name': i['permission']['name'],
                    'route': i['permission']['route'],
                    'method': i['permission']['method']
                }
                list_method_route.append(method_role)
        return list_method_route