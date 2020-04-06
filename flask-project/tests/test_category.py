import unittest
from faker import Faker

from FlaskProject import create_app, db, TestCategory, FlaskProjectLogException
from FlaskProject.general import Status

from FlaskProject.controllers.test_category_controller.controller import \
    TestCategoryController


class TestTestCategoryController(unittest.TestCase):
    """
    This class is for testing TestCategoryController
    """

    def setUp(self):
        """
        Method for setUp TestCategoryController test module
        :return: OK or ERROR
        """
        self.app = create_app('development')
        self.app.testing = True
        self.client = self.app.test_client()
        self.ctx = self.app.app_context()
        self.ctx.push()

        self.faker = Faker()

        self.test_category_controller = TestCategoryController(
            test_category=TestCategory(
                name=self.faker.name()
            ))

    def test_create(self):
        """
        Method for testing creation of categories
        :return: OK or ERROR
        """

        status_insert = self.test_category_controller.create()

        self.assertEqual(
            Status.status_successfully_inserted().__dict__, status_insert)

        self.assertIsNotNone(self.test_category_controller.test_category.id)

    def test_create_already_exist(self):
        """
        Method for testing creation of categories when name is already taken
        :return: OK or ERROR
        """
        self.test_category_controller.create()
        with self.assertRaises(FlaskProjectLogException):
            self.test_category_controller.create()

    def test_alter(self):
        """
        Method for testing categories updates
        :return: OK or ERROR
        """

        self.test_category_controller.create()

        name = self.faker.name()
        self.test_category_controller.test_category.name = name

        result = self.test_category_controller.alter()

        self.assertEqual(Status.status_update_success().__dict__,
                         result)

        self.assertEqual(name, self.test_category_controller.test_category.name)

    def test_inactivate(self):
        """
        Method for testing categories inactivate
        :return: OK OR ERROR
        """

        self.test_category_controller.create()
        result = self.test_category_controller.inactivate()

        self.assertEqual(Status.status_successfully_processed().__dict__,
                         result)

        self.assertEqual(TestCategory.STATUSES['inactive'],
                         self.test_category_controller.test_category.status)

    def test_activate(self):
        """
        Method for testing categories activate
        :return: OK OR ERROR
        """

        self.test_category_controller.create()
        result = self.test_category_controller.activate()

        self.assertEqual(Status.status_successfully_processed().__dict__,
                         result)

        self.assertEqual(TestCategory.STATUSES['active'],
                         self.test_category_controller.test_category.status)

    def test_get_one(self):
        """
        Method for testing get one category by identifier
        :return: OK OR ERROR
        """

        self.test_category_controller.create()

        result = TestCategoryController.get_one(
            self.test_category_controller.test_category.id)

        self.assertEqual(str(self.test_category_controller.test_category.id),
                         str(result.test_category.id))

    def test_list_autocomplete(self):
        """
        Method for testing categories autocomplete
        :return: OK OR ERROR
        """
        self.test_category_controller.create()

        result = TestCategoryController.list_autocomplete(
            self.test_category_controller.test_category.name)

        self.assertEqual(list, type(result))

        self.assertIn(str(self.test_category_controller.test_category.id),
                      [d['id'] for d in result])

    def test_get_list_pagination(self):
        """"
        Method for testing get list of all categories with pagination
        :return: OK or Error
        """

        self.test_category_controller.create()

        result = TestCategoryController.get_list_pagination(
            start=0, limit=10,
            name=self.test_category_controller.test_category.name)
        self.assertEqual(
            Status.status_successfully_processed().__dict__, result['status'])
        self.assertEqual(
            int, type(result['total']))
        self.assertEqual(
            list, type(result['data']))
        self.assertIn(str(self.test_category_controller.test_category.id),
                      [d['id'] for d in result['data']])


    def tearDown(self):
        """
        Method for clean up data
        :return: OK or ERROR
        """
        TestCategory.query.filter(
            TestCategory.id ==
            self.test_category_controller.test_category.id).delete()
        db.session.commit()


if __name__ == '__main__':
    unittest.main()
