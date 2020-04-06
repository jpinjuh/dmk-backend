from sqlalchemy import and_

from ... import TestCategory, FlaskProjectLogException
from ...controllers.base_controller import BaseController
from ...general import Status, obj_to_dict


class TestCategoryController(BaseController):

    def __init__(self, test_category=TestCategory()):
        self.test_category = test_category

    def create(self):
        """
        Method used for creating categories
        :return: Status object or raise FlaskProjectLogException
        """

        if TestCategory.query.check_if_already_exist_by_name(
                self.test_category.name):
            raise FlaskProjectLogException(
                Status.status_test_category_already_exist())

        self.test_category.add()
        self.test_category.commit_or_rollback()

        return Status.status_successfully_inserted().__dict__

    def alter(self):
        """
        Method used for updating categories
        :return: Status object or raise FlaskProjectLogException
        """

        test_category = TestCategory.query.get_one(self.test_category.id)

        if test_category is None:
            raise FlaskProjectLogException(
                Status.status_test_category_not_exist())

        if TestCategory.query.check_if_name_is_taken(
                test_category.id, self.test_category.name):
            raise FlaskProjectLogException(
                Status.status_test_category_already_exist())

        test_category.name = self.test_category.name
        test_category.update()
        test_category.commit_or_rollback()

        self.test_category = test_category

        return Status.status_update_success().__dict__

    def inactivate(self):
        """
        Method used for setting test categories status to inactive (0)
        :return: Status object or raise FlaskProjectLogException
        """
        test_category = TestCategory.query.get_one(self.test_category.id)

        if test_category is None:
            raise FlaskProjectLogException(
                Status.status_test_category_not_exist())

        test_category.status = TestCategory.STATUSES['inactive']

        test_category.update()
        test_category.commit_or_rollback()

        self.test_category = test_category

        return Status.status_successfully_processed().__dict__

    def activate(self):
        """
        Method used for setting test categories status to active (1)
        :return: Status object or raise FlaskProjectLogException
        """
        test_category = TestCategory.query.get_one(self.test_category.id)

        if test_category is None:
            raise FlaskProjectLogException(
                Status.status_test_category_not_exist())

        if TestCategory.query.check_if_name_is_taken(
                test_category.id, self.test_category.name):
            raise FlaskProjectLogException(
                Status.status_test_category_already_exist())

        test_category.status = TestCategory.STATUSES['active']

        test_category.update()
        test_category.commit_or_rollback()

        self.test_category = test_category

        return Status.status_successfully_processed().__dict__

    @classmethod
    def get_one(cls, identifier):
        """
        Use this method to get an test category by identifier
        :param identifier: Extras Category identifier
        :return: TestCategoryController object
        """

        return cls(test_category=TestCategory.query.get_one(identifier))

    @staticmethod
    def get_one_details(identifier):
        """
        Use this method to get an test category by identifier
        :param identifier: Test Category identifier
        :return: Dict object
        """
        test_category = TestCategory.query.get_one(identifier)

        if test_category is not None:
            return obj_to_dict(test_category)

    @staticmethod
    def list_autocomplete(search):
        """
        Method for searching categories with autocomplete
        :param search: Data for search
        :return: List of dicts
        """
        list_data = []
        if search:
            test_category = TestCategory.query.autocomplete_by_name(search)
            for i in test_category:
                list_data.append(obj_to_dict(i))

        return list_data

    @staticmethod
    def get_list_pagination(start, limit, **kwargs):
        """
        Method for getting all categories by filter_data in pagination form
        :return: dict with total, data and status
        """

        filter_main = and_(
            TestCategory.status == TestCategory.STATUSES['active'])

        name = kwargs.get('name', None)

        if name:
            filter_main = and_(
                filter_main, TestCategory.name.ilike('%'+name+'%'))

        data = TestCategory.query.filter(
            filter_main).order_by(TestCategory.created_at.asc()).paginate(
            page=start, error_out=False, per_page=limit)

        total = data.total
        list_data = []

        for i in data.items:
            list_data.append(obj_to_dict(i))

        return dict(
            status=Status.status_successfully_processed().__dict__,
            total=total, data=list_data)
