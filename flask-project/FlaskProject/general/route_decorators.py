from flask import jsonify, request, current_app, url_for, redirect
from ..flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity, get_jwt_claims
)
from functools import wraps
from ..general import Status
import jwt
from ..controllers.privileges_controller.controller import PrivilegeController
from ..models import Permission


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
            ##token = request.args.get('token')
            ##token = request.headers['HTTP_AUTHORIZATION']
            ##Ovdje ide programski kod za validaciju jwt

            if token:
                current_role = get_jwt_claims()['roles_id']
                permissions = PrivilegeController.get_role_permissions(current_role)
                permission = None
                for obj in permissions:
                    if obj['route'] == request.url_rule.rule and obj['method'] == request.method:
                        permission = obj['name']
                        break
                if permission is None:
                    return jsonify(status=Status.status_access_denied().__dict__)

        except Exception as e:
            return jsonify(status=Status.status_token_required().__dict__)

        return function(*args, **kwargs)
    return decorated_function





