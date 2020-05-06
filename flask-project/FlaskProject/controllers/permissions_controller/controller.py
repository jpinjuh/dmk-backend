from sqlalchemy import and_

from ... import Permission, FlaskProjectLogException
from ...controllers.base_controller import BaseController
from ...general import Status, obj_to_dict
from ...models import User

class PermissionController(BaseController):

    def __init__(self, permission=Permission()):
        self.permission = permission

    def create(self):
        """
        Method used for creating permissions
        :return: Status object or raise FlaskProjectLogException
        """

        if Permission.query.check_if_already_exist(
                self.permission.route, self.permission.method):
            raise FlaskProjectLogException(
                Status.status_permission_already_exist())

        self.permission.add()
        self.permission.commit_or_rollback()

        return Status.status_successfully_inserted().__dict__

    def alter(self):
        """
        Method used for updating permissions
        :return: Status object or raise FlaskProjectLogException
        """

        permission = Permission.query.get_one(self.permission.id)

        if permission is None:
            raise FlaskProjectLogException(
                Status.status_permission_not_exist())

        if Permission.query.check_if_name_is_taken(
                permission.id, self.permission.name):
            raise FlaskProjectLogException(
                Status.status_permission_already_exist())

        permission.name = self.permission.name
        permission.route = self.permission.route
        permission.method = self.permission.method
        permission.update()
        permission.commit_or_rollback()

        self.permission = permission

        return Status.status_update_success().__dict__

    def inactivate(self):
        """
        Method used for setting permissions status to inactive (0)
        :return: Status object or raise FlaskProjectLogException
        """
        permission = Permission.query.get_one(self.permission.id)

        if permission is None:
            raise FlaskProjectLogException(
                Status.status_permission_not_exist())

        permission.status = Permission.STATUSES['inactive']

        permission.update()
        permission.commit_or_rollback()

        self.permission = permission

        return Status.status_successfully_processed().__dict__

    def activate(self):
        """
        Method used for setting permissions status to active (1)
        :return: Status object or raise FlaskProjectLogException
        """
        permission = Permission.query.get_one(self.permission.id)

        if permission is None:
            raise FlaskProjectLogException(
                Status.status_permission_not_exist())

        if Permission.query.check_if_name_is_taken(
                permission.id, self.permission.name):
            raise FlaskProjectLogException(
                Status.status_permission_already_exist())

        permission.status = Permission.STATUSES['active']

        permission.update()
        permission.commit_or_rollback()

        self.permission = permission

        return Status.status_successfully_processed().__dict__

    @classmethod
    def get_one(cls, identifier):
        """
        Use this method to get an permission by identifier
        :param identifier: Extras Permission identifier
        :return: PermissionController object
        """

        return cls(permission=Permission.query.get_one(identifier))

    @staticmethod
    def get_one_details(identifier):
        """
        Use this method to get an permission by identifier
        :param identifier: Permission identifier
        :return: Dict object
        """
        permission = Permission.query.get_one(identifier)

        if permission is not None:
            return obj_to_dict(permission)

    @staticmethod
    def list_autocomplete(search):
        """
        Method for searching permissions with autocomplete
        :param search: Data for search
        :return: List of dicts
        """
        list_data = []
        if search:
            permission = Permission.query.autocomplete_by_name(search)
            for i in permission:
                list_data.append(obj_to_dict(i))

        return list_data

    @staticmethod
    def get_list_pagination(start, limit, **kwargs):
        """
        Method for getting all permissions by filter_data in pagination form
        :return: dict with total, data and status
        """

        filter_main = and_()
            #Permission.status == Permission.STATUSES['active'])

        name = kwargs.get('name', None)

        if name:
            filter_main = and_(
                filter_main, Permission.name.ilike('%'+name+'%'))

        data = Permission.query.filter(
            filter_main).order_by(Permission.created_at.asc()).paginate(
            page=start, error_out=False, per_page=limit)

        total = data.total
        list_data = []

        for i in data.items:
            list_data.append(obj_to_dict(i))

        return dict(
            status=Status.status_successfully_processed().__dict__,
            total=total, data=list_data)




