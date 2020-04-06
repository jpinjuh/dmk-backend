from flask import request, jsonify

from .controller import TestCategoryController
from ... import bpp, TestCategory, FlaskProjectLogException
from ...general import Status, obj_to_dict
from ...general.route_decorators import allow_access
from ...schema import TestCategorySchema


@bpp.route('/testCategory', methods=['POST'])
@allow_access
def create_test_category():
    request_json = request.get_json()
    schema = TestCategorySchema(exclude=('id',))

    params = schema.load(request_json)

    controller = TestCategoryController(
        test_category=TestCategory(
            name=params['name']
        ))
    controller.create()

    return jsonify(
        data=obj_to_dict(controller.test_category),
        status=Status.status_successfully_inserted().__dict__)


@bpp.route('/testCategory/<string:test_category_id>', methods=['PUT'])
@allow_access
def alter_test_category(test_category_id):
    request_json = request.get_json()
    schema = TestCategorySchema(exclude=('id',))

    params = schema.load(request_json)

    controller = TestCategoryController(
        test_category=TestCategory(
            id=test_category_id,
            name=params['name']
        ))
    controller.alter()

    return jsonify(
        data=obj_to_dict(controller.test_category),
        status=Status.status_update_success().__dict__)


@bpp.route('/testCategory/<string:test_category_id>', methods=['DELETE'])
@allow_access
def test_category_inactivate(test_category_id):
    controller = TestCategoryController(
        test_category=TestCategory(id=test_category_id))

    controller.inactivate()

    return jsonify(
        data=obj_to_dict(controller.test_category),
        status=Status.status_successfully_processed().__dict__)


@bpp.route('/testCategory/activate', methods=['POST'])
@allow_access
def test_category_activate():
    request_json = request.get_json()
    schema = TestCategorySchema(only=('id',))

    params = schema.load(request_json)
    controller = TestCategoryController(
        test_category=TestCategory(id=params['id']))

    controller.activate()

    return jsonify(
        data=obj_to_dict(controller.test_category),
        status=Status.status_successfully_processed().__dict__)


@bpp.route('/testCategory/<string:test_category_id>', methods=['GET'])
@allow_access
def get_one_test_category(test_category_id):
    controller = TestCategoryController.get_one_details(test_category_id)

    if controller is None:
        raise FlaskProjectLogException(Status.status_test_category_not_exist())

    return jsonify(
        data=controller,
        status=Status.status_successfully_processed().__dict__)


@bpp.route('/testCategory/autocomplete', methods=['POST'])
@allow_access
def test_category_autocomplete():
    request_json = request.get_json()
    search = request_json.get('search', None)

    data = TestCategoryController.list_autocomplete(search)

    return jsonify(
        data=data,
        status=Status.status_successfully_processed().__dict__)


@bpp.route('/testCategory', methods=['GET'])
@allow_access
def get_test_categories():
    start = request.args.get('start', 0, int)
    limit = request.args.get('limit', 20, int)
    name = request.args.get('name', None, str)

    pagination_result = TestCategoryController.get_list_pagination(
        start=start, limit=limit, name=name)

    return jsonify(pagination_result)


