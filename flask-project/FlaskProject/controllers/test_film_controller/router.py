from flask import request, jsonify

from .controller import TestFilmController
from ... import bpp, TestFilm, FlaskProjectLogException
from ...general import Status
from ...general.route_decorators import allow_access
from ...schema import TestFilmSchema


@bpp.route('/testFilm', methods=['POST'])
@allow_access
def create_test_film():
    request_json = request.get_json()
    schema = TestFilmSchema(exclude=('id',))

    params = schema.load(request_json)

    controller = TestFilmController(
        test_film=TestFilm(
            name=params['name'],
            test_category_id=params['test_category']['id']
        ))

    controller.create()

    return jsonify(
        data=TestFilmController.get_one_details(controller.test_film.id),
        status=Status.status_successfully_inserted().__dict__)


@bpp.route('/testFilm/<string:test_film_id>', methods=['GET'])
@allow_access
def get_one_test_film(test_film_id):
    controller = TestFilmController.get_one_details(test_film_id)

    if controller is None:
        raise FlaskProjectLogException(Status.status_test_film_not_exist())

    return jsonify(
        data=controller,
        status=Status.status_successfully_processed().__dict__)


@bpp.route('/testFilm/autocomplete', methods=['POST'])
@allow_access
def test_film_autocomplete():
    request_json = request.get_json()
    search = request_json.get('search', None)

    data = TestFilmController.list_autocomplete(search)

    return jsonify(
        data=data,
        status=Status.status_successfully_processed().__dict__)


@bpp.route('/testFilm', methods=['GET'])
@allow_access
def get_test_films():
    start = request.args.get('start', 0, int)
    limit = request.args.get('limit', 20, int)

    film_name = request.args.get('film_name', '', str)
    category_id = request.args.get('category_id', None, str)

    pagination_result = TestFilmController.get_list_pagination(
        start=start, limit=limit, film_name=film_name,
        category_id=category_id)

    return jsonify(pagination_result)
