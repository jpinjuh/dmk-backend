from abc import ABC, abstractmethod


class BaseController(ABC):

    @abstractmethod
    def create(self):
        pass

    @abstractmethod
    def alter(self):
        pass

    @abstractmethod
    def inactivate(self):
        pass

    @abstractmethod
    def activate(self):
        pass

    @classmethod
    @abstractmethod
    def get_one(cls, identifier):
        pass

    @staticmethod
    @abstractmethod
    def get_one_details(identifier):
        pass

    @staticmethod
    @abstractmethod
    def list_autocomplete(search):
        pass

    @staticmethod
    @abstractmethod
    def get_list_pagination(start, limit, **kwargs):
        pass

