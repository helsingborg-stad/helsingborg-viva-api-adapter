from flask import current_app
from flask_restful import Api
from werkzeug.http import HTTP_STATUS_CODES
from werkzeug.exceptions import HTTPException
from requests.exceptions import ConnectionError
from marshmallow.exceptions import ValidationError as MarshmallowValidationError

from app.errors.viva_request_error import VivaRequestError


class CustomFlaskRestfulApi(Api):

    def handle_error(self, error):
        current_app.logger.error(msg=error.message)

        if isinstance(error, HTTPException):
            details = error.description
            return self._error_response(status_code=error.code, details=details)

        if isinstance(error, ConnectionError):
            details = error.strerror
            status_code = 502
            return self._error_response(status_code=status_code, details=details)

        if isinstance(error, VivaRequestError):
            details = error.message
            return self._error_response(status_code=error.http_status_code, details=details)

        if isinstance(error, MarshmallowValidationError):
            details = error.messages
            status_code = 400
            return self._error_response(status_code=status_code, details=details)

        if not getattr(error, 'message', None):
            details = f'Server has encountered an unexpected error: {error}'
            status_code = 500
            return self._error_response(status_code=status_code, details=details)

        # Handle application specific custom exceptions
        return dict(**error.kwargs), error.http_status_code

    def _error_response(self, status_code, details):
        description = HTTP_STATUS_CODES.get(status_code, '')

        response = {
            'error': {
                'code': status_code,
                'description': description,
                'details': details,
            }
        }

        return response, status_code
