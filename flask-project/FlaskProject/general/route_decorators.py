from flask import jsonify, request
from functools import wraps
from ..general import Status


def allow_access(function):
    """
    allow_access decorator that requires a valid permission

    :param function: function parameter
    :return: decorated_function

    """
    @wraps(function)
    def decorated_function(*args, **kwargs):
        """
        allow_access route that requires a valid permission
        :param args:
        :param kwargs:
        :return: Decorated function
        """

        try:
            token = request.headers.environ['HTTP_AUTHORIZATION']
            ##Ovdje ide programski kod za validaciju jwt

        except Exception as e:
            return jsonify(stattus=Status.status_token_required().__dict__)

        return function(*args, **kwargs)

    return decorated_function





