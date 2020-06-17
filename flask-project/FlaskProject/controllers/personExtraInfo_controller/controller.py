from sqlalchemy import and_

from ... import PersonExtraInfo, FlaskProjectLogException, Person
from ...controllers.base_controller import BaseController
from ...general import Status, obj_to_dict


class PersonExtraInfoController(BaseController):

    def __init__(self, extra_info=PersonExtraInfo()):
        self.extra_info = extra_info

    def create(self):
        """
        Method used for creating person extra info
        :return: Status object or raise FlaskProjectLogException
        """

        self.extra_info.add()
        self.extra_info.commit_or_rollback()

        return Status.status_successfully_inserted().__dict__

    def alter(self):
        raise NotImplementedError("To be implemented")

    def inactivate(self):
        raise NotImplementedError("To be implemented")

    def activate(self):
        raise NotImplementedError("To be implemented")

    @classmethod
    def get_one(cls, identifier):
        return cls(extra_info=PersonExtraInfo.query.get_one(identifier))

    @staticmethod
    def get_one_details(identifier):
        """
       Use this method to get an person extra info by identifier
       :param identifier: List item identifier
       :return: Dict object
       """
        raise NotImplementedError("To be implemented")

    @staticmethod
    def list_autocomplete(search):
        """
        Method for searching person extra info with autocomplete
        :param search:Data for search
        :return: List of dicts
        """
        raise NotImplementedError("To be implemented")

    @staticmethod
    def get_list_pagination(start, limit, **kwargs):
        raise NotImplementedError("To be implemented")

    @staticmethod
    def __custom_sql(row_data):
        if row_data is not None:
            return_dict = obj_to_dict(row_data.PersonExtraInfo)
            return return_dict
        return None