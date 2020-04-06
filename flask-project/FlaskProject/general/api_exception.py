import logging
import requests
from flask import jsonify
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError
from . import FlaskProjectLogException
from ..general import Status

logger = logging.getLogger('FlaskProject')


class ApiExceptionHandler:
    @classmethod
    def calculate_http_status(cls, exception):
        http_response_code = requests.codes.SERVER_ERROR

        if hasattr(exception, 'status_code'):
            http_response_code = exception.status_code
        elif hasattr(exception, 'code'):
            http_response_code = exception.code
        else:
            if isinstance(exception, IntegrityError):
                http_response_code = requests.codes.BAD_REQUEST
            elif isinstance(exception, ValidationError):
                http_response_code = requests.codes.BAD_REQUEST
            elif isinstance(exception, FlaskProjectLogException):
                http_response_code = exception.status.errorCode

        #     TODO - Add more exception types if/when needed

        return http_response_code

    @classmethod
    def calculate_message(cls, exception, message=None):
        if exception and isinstance(exception, IntegrityError):
            # Try to get original message from SQLAlchemy exception
            # Since this exception is adapter speciffic, following will work
            # only for PostgreSQL adapter
            pg_orig = getattr(exception, 'orig', None)
            if pg_orig:
                # pgcode = getattr(pg_orig, 'pgcode', None)
                diag = getattr(pg_orig, 'diag', None)
                if diag:
                    # message = getattr(diag, 'message_detail', '')
                    #message = getattr(diag, 'message_primary', '')
                    message = Status.something_went_wrong().description

        if (
            exception and
            hasattr(exception, 'description') and
            exception.description
        ):
            return exception.description

        if isinstance(exception, FlaskProjectLogException):
            return exception.status.description

        return (
            message or
            (str(exception) if exception else '') or
            ''
        ).replace('"', "'")


def build_and_log_error_dict(exception, message=None):
    """Builds error dictionary form exception and optional message."""

    exception_dict = dict()
    if isinstance(exception, ValidationError):
        exception_dict['description'] = exception.messages
    else:
        exception_dict['description'] = \
            ApiExceptionHandler.calculate_message(exception, message)

    exception_dict['errorCode'] = \
        ApiExceptionHandler.calculate_http_status(exception)
    return exception_dict


def build_error_response(exception):
    """
    Builds JSON response from error dictionary.
    """
    response = jsonify(status=build_and_log_error_dict(exception.exception))
    response.status_code = 200

    if response.json['status']['errorCode'] == -101:
        response = jsonify(status=Status.something_went_wrong().__dict__)
        response.status_code = 200

    return response
