from sqlalchemy import and_

from ..test_category_controller.controller import TestCategoryController
from ... import TestFilm, FlaskProjectLogException, TestCategory
from ...controllers.base_controller import BaseController
from ...general import Status, obj_to_dict


class TestFilmController(BaseController):
    def __init__(self, test_film=TestFilm()):
        self.test_film = test_film

    def create(self):
        """
         Method used for creating film
        :return: Status object or raise FlaskProjectLogException
        """

        if self.test_film.test_category_id is not None:
            category = TestCategoryController.get_one(
                self.test_film.test_category_id)

            if category.test_category is None:
                raise FlaskProjectLogException(
                    Status.status_test_category_not_exist())

        self.test_film.add()
        self.test_film.commit_or_rollback()

        return Status.status_successfully_inserted().__dict__

    def alter(self):
        raise NotImplementedError("To be implemented")

    def inactivate(self):
        raise NotImplementedError("To be implemented")

    def activate(self):
        raise NotImplementedError("To be implemented")

    @classmethod
    def get_one(cls, identifier):
        return cls(test_film=TestFilm.query.get_one(identifier))

    @staticmethod
    def get_one_details(identifier):
        """
       Use this method to get an test film by identifier
       :param identifier: Test film identifier
       :return: Dict object
       """
        return TestFilmController.__custom_sql(
            TestFilm.query.get_one_details(identifier))

    @staticmethod
    def list_autocomplete(search):
        """
        Method for searching films with autocomplete
        :param search:Data for search
        :return: List of dicts
        """
        list_data = []
        if search:
            test_category = TestFilm.query.autocomplete_by_name(search)
            for i in test_category:
                list_data.append(TestFilmController.__custom_sql(i))

        return list_data

    @staticmethod
    def get_list_pagination(start, limit, **kwargs):
        """
        Method for getting all films by filter_data in pagination form
        :return: dict with total, data and status
        """

        filter_main = and_()

        film_name = kwargs.get('film_name', None)
        category_id = kwargs.get('category_id', None)

        if film_name:
            filter_main = and_(
                filter_main, TestFilm.name.ilike('%' + film_name + '%'))

        if category_id:
            filter_main = and_(
                filter_main, TestCategory.id == category_id)

        data = TestFilm.query.get_all_by_filter(filter_main).paginate(
            page=start, error_out=False, per_page=limit)

        total = data.total
        list_data = []

        for i in data.items:
            list_data.append(TestFilmController.__custom_sql(i))

        return dict(
            status=Status.status_successfully_processed().__dict__,
            total=total, data=list_data)

    @staticmethod
    def __custom_sql(row_data):
        if row_data is not None:
            return_dict = obj_to_dict(row_data.TestFilm)
            return_dict['category'] = obj_to_dict(row_data.TestCategory)
            return return_dict
        return None
