import unittest
from faker import Faker

from FlaskProject import create_app, db, TestFilm, TestCategory
from FlaskProject.general import Status

from FlaskProject.controllers.test_film_controller.controller import \
    TestFilmController


class TestTestCategoryController(unittest.TestCase):
    """
    This class is for testing TestFilmController
    """

    def setUp(self):
        """
        Method for setUp TestFilmController test module
        :return: OK or ERROR
        """
        self.app = create_app('development')
        self.app.testing = True
        self.client = self.app.test_client()
        self.ctx = self.app.app_context()
        self.ctx.push()

        self.faker = Faker()

        self.test_category = TestCategory(
            name=self.faker.name()
        )

        self.test_film_controller = TestFilmController(
            test_film=TestFilm(
                name=self.faker.name()
            ))

    def test_create(self):
        """
        Method for testing creation of film
        :return: OK or ERROR
        """
        db.session.add(self.test_category)
        db.session.commit()

        self.test_film_controller.test_film.test_category_id = \
            self.test_category.id

        status_insert = self.test_film_controller.create()

        self.assertEqual(
            Status.status_successfully_inserted().__dict__, status_insert)

        self.assertIsNotNone(self.test_film_controller.test_film.id)

    def test_get_one(self):
        """
        Method for testing get one film by identifier
        :return: OK OR ERROR
        """

        db.session.add(self.test_category)
        db.session.commit()

        self.test_film_controller.test_film.test_category_id = \
            self.test_category.id

        self.test_film_controller.create()

        result = TestFilmController.get_one(
            self.test_film_controller.test_film.id)

        self.assertEqual(str(self.test_film_controller.test_film.id),
                         str(result.test_film.id))

    def test_list_autocomplete(self):
        """
        Method for testing films autocomplete
        :return: OK OR ERROR
        """
        db.session.add(self.test_category)
        db.session.commit()

        self.test_film_controller.test_film.test_category_id = \
            self.test_category.id

        self.test_film_controller.create()

        result = TestFilmController.list_autocomplete(
            self.test_film_controller.test_film.name)

        self.assertEqual(list, type(result))

        self.assertIn(str(self.test_film_controller.test_film.id),
                      [d['id'] for d in result])

    def test_get_list_pagination(self):
        """"
        Method for testing get list of all films with pagination
        :return: OK or Error
        """

        db.session.add(self.test_category)
        db.session.commit()

        self.test_film_controller.test_film.test_category_id = \
            self.test_category.id

        self.test_film_controller.create()

        result = TestFilmController.get_list_pagination(
            start=0, limit=10,
            film_name=self.test_film_controller.test_film.name,
            category_id=self.test_category.id)

        self.assertEqual(
            Status.status_successfully_processed().__dict__, result['status'])
        self.assertEqual(
            int, type(result['total']))
        self.assertEqual(
            list, type(result['data']))
        self.assertIn(str(self.test_film_controller.test_film.id),
                      [d['id'] for d in result['data']])


    def tearDown(self):
        """
        Method for clean up data
        :return: OK or ERROR
        """
        TestFilm.query.filter(
            TestFilm.id == self.test_film_controller.test_film.id).delete()

        TestCategory.query.filter(
            TestCategory.id ==
            self.test_category.id).delete()

        db.session.commit()


if __name__ == '__main__':
    unittest.main()
