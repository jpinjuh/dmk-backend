from sqlalchemy import and_

from ... import Role, FlaskProjectLogException
from ...controllers.base_controller import BaseController
from ...general import Status, obj_to_dict


class RoleController(BaseController):

    def __init__(self, role=Role()):
        self.role = role

    def create(self):
        """
        Method used for creating roles
        :return: Status object or raise FlaskProjectLogException
        """

        if Role.query.check_if_already_exist_by_name(
                self.role.name):
            raise FlaskProjectLogException(
                Status.status_role_already_exist())

        self.role.add()
        self.role.commit_or_rollback()

        return Status.status_successfully_inserted().__dict__

    def alter(self):
        """
        Method used for updating roles
        :return: Status object or raise FlaskProjectLogException
        """

        role = Role.query.get_one(self.role.id)

        if role is None:
            raise FlaskProjectLogException(
                Status.status_role_not_exist())

        if Role.query.check_if_name_is_taken(
                role.id, self.role.name):
            raise FlaskProjectLogException(
                Status.status_role_already_exist())

        role.name = self.role.name
        role.update()
        role.commit_or_rollback()

        self.role = role

        return Status.status_update_success().__dict__

    def inactivate(self):
        """
        Method used for setting roles status to inactive (0)
        :return: Status object or raise FlaskProjectLogException
        """
        role = Role.query.get_one(self.role.id)

        if role is None:
            raise FlaskProjectLogException(
                Status.status_role_not_exist())

        role.status = Role.STATUSES['inactive']

        role.update()
        role.commit_or_rollback()

        self.role = role

        return Status.status_successfully_processed().__dict__

    def activate(self):
        """
        Method used for setting roles status to active (1)
        :return: Status object or raise FlaskProjectLogException
        """
        role = Role.query.get_one(self.role.id)

        if role is None:
            raise FlaskProjectLogException(
                Status.status_role_not_exist())

        if Role.query.check_if_name_is_taken(
                role.id, self.role.name):
            raise FlaskProjectLogException(
                Status.status_role_already_exist())

        role.status = Role.STATUSES['active']

        role.update()
        role.commit_or_rollback()

        self.role = role

        return Status.status_successfully_processed().__dict__

    @classmethod
    def get_one(cls, identifier):
        """
        Use this method to get an role by identifier
        :param identifier: Extras Role identifier
        :return: RoleController object
        """

        return cls(role=Role.query.get_one(identifier))

    @staticmethod
    def get_one_details(identifier):
        """
        Use this method to get an role by identifier
        :param identifier: Role identifier
        :return: Dict object
        """
        role = Role.query.get_one(identifier)

        if role is not None:
            return obj_to_dict(role)

    @staticmethod
    def list_autocomplete(search):
        """
        Method for searching roles with autocomplete
        :param search: Data for search
        :return: List of dicts
        """
        list_data = []
        if search:
            role = Role.query.autocomplete_by_name(search)
            for i in role:
                list_data.append(obj_to_dict(i))

        return list_data

    @staticmethod
    def get_list_pagination(start, limit, **kwargs):
        """
        Method for getting all roles by filter_data in pagination form
        :return: dict with total, data and status
        """

        filter_main = and_()
            #Role.status == Role.STATUSES['active'])

        name = kwargs.get('name', None)

        if name:
            filter_main = and_(
                filter_main, Role.name.ilike('%'+name+'%'))

        data = Role.query.filter(
            filter_main).order_by(Role.created_at.asc()).paginate(
            page=start, error_out=False, per_page=limit)

        total = data.total
        list_data = []

        for i in data.items:
            list_data.append(obj_to_dict(i))

        return dict(
            status=Status.status_successfully_processed().__dict__,
            total=total, data=list_data)

    @staticmethod
    def get_all():
        roles = Role.query.order_by(Role.created_at.asc()).all()

        list_data = []

        for role in roles:
            list_data.append(obj_to_dict(role))

        return dict(
            status=Status.status_successfully_processed().__dict__,
            data=list_data)