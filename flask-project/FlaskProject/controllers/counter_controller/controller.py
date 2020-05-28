from sqlalchemy import and_

from ... import Counter, FlaskProjectLogException
from ...controllers.base_controller import BaseController
from ...general import Status, obj_to_dict


class CounterController(BaseController):

    def __init__(self, counter=Counter()):
        self.counter = counter

    def create(self):
        """
        Method used for creating counter
        :return: Status object or raise FlaskProjectLogException
        """

        if Counter.query.check_if_already_exist_by_name(
                self.counter.name):
            raise FlaskProjectLogException(
                Status.status_counter_already_exist())

        self.counter.add()
        self.counter.commit_or_rollback()

        return Status.status_successfully_inserted().__dict__

    def alter(self):
        raise NotImplementedError("To be implemented")

    def inactivate(self):
        raise NotImplementedError("To be implemented")

    def activate(self):
        raise NotImplementedError("To be implemented")

    @classmethod
    def get_one(cls, identifier):
        """
        Use this method to get a counter by identifier
        :param identifier: Extras State identifier
        :return: CounterController object
        """

        return cls(counter=Counter.query.get_one(identifier))

    @staticmethod
    def get_one_details(identifier):
        raise NotImplementedError("To be implemented")

    @staticmethod
    def list_autocomplete(search):
        raise NotImplementedError("To be implemented")

    @staticmethod
    def get_list_pagination(start, limit, **kwargs):
        raise NotImplementedError("To be implemented")
