from sqlalchemy import and_

from ... import List, FlaskProjectLogException
from ...controllers.base_controller import BaseController
from ...general import Status, obj_to_dict


class ListController(BaseController):

    def __init__(self, list=List()):
        self.list = list

    def create(self):
        """
        Method used for creating lists
        :return: Status object or raise FlaskProjectLogException
        """

        if List.query.check_if_already_exist_by_name(
                self.list.name):
            raise FlaskProjectLogException(
                Status.status_list_already_exist())

        self.list.add()
        self.list.commit_or_rollback()

        return Status.status_successfully_inserted().__dict__

    def alter(self):
        """
        Method used for updating lists
        :return: Status object or raise FlaskProjectLogException
        """

        list = List.query.get_one(self.list.id)

        if list is None:
            raise FlaskProjectLogException(
                Status.status_list_not_exist())

        if List.query.check_if_name_is_taken(
                list.id, self.list.name):
            raise FlaskProjectLogException(
                Status.status_list_already_exist())

        list.name = self.list.name
        list.update()
        list.commit_or_rollback()

        self.list = list

        return Status.status_update_success().__dict__

    def inactivate(self):
        raise NotImplementedError("To be implemented")

    def activate(self):
        """
        Method used for setting roles status to active (1)
        :return: Status object or raise FlaskProjectLogException
        """
        raise NotImplementedError("To be implemented")

    @classmethod
    def get_one(cls, identifier):
        """
        Use this method to get an list by identifier
        :param identifier: Extras List identifier
        :return: ListController object
        """

        return cls(list=List.query.get_one(identifier))

    @staticmethod
    def get_one_details(identifier):
        """
        Use this method to get an list by identifier
        :param identifier: List identifier
        :return: Dict object
        """
        raise NotImplementedError("To be implemented")

    @staticmethod
    def list_autocomplete(search):
        """
        Method for searching lists with autocomplete
        :param search: Data for search
        :return: List of dicts
        """
        raise NotImplementedError("To be implemented")

    @staticmethod
    def list_search(search):
        """
        Method for searching lists
        :param search: Data for search
        :return: List of dicts
        """
        raise NotImplementedError("To be implemented")

    @staticmethod
    def get_list_pagination(start, limit, **kwargs):
        """
        Method for getting all lists by filter_data in pagination form
        :return: dict with total, data and status
        """

        filter_main = and_()
            #List.status == List.STATUSES['active'])

        name = kwargs.get('name', None)

        if name:
            filter_main = and_(
                filter_main, List.name.ilike('%'+name+'%'))

        data = List.query.filter(
            filter_main).order_by(List.created_at.asc()).paginate(
            page=start, error_out=False, per_page=limit)

        total = data.total
        list_data = []

        for i in data.items:
            list_data.append(obj_to_dict(i))

        return dict(
            status=Status.status_successfully_processed().__dict__,
            total=total, data=list_data)


