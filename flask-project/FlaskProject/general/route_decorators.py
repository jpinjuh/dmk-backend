from flask import jsonify, request, current_app
from ..flask_jwt_extended import jwt_required, get_jwt_identity
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
            #token = request.args.get('token')
            #token = request.headers['HTTP_AUTHORIZATION']
            ##Ovdje ide programski kod za validaciju jwt

            #data = jwt.decode(token, current_app.config.get('JWT_SECRET_KEY'))
            #current_user = Users.query.filter_by(username=data['username']).first()
            #current_user = get_jwt_identity()
        except Exception as e:
            return jsonify(stattus=Status.status_token_required().__dict__)

        return function(*args, **kwargs)

    return decorated_function





