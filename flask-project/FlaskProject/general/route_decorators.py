from flask import jsonify, request, current_app
from functools import wraps
from ..general import Status
import jwt

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
            data = jwt.decode(token, current_app.config.get('JWT_SECRET_KEY'))
            current_user = Users.query.filter_by(username=data['username']).first()


        except Exception as e:
            return jsonify(stattus=Status.status_token_required().__dict__)

        return function(current_user, *args, **kwargs)

    return decorated_function





