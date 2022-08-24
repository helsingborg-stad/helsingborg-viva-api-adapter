from flask_restful import Api
from werkzeug.http import HTTP_STATUS_CODES
from werkzeug.exceptions import HTTPException
from requests.exceptions import ConnectionError
from marshmallow.exceptions import ValidationError as MarshmallowValidationError

from app.errors.viva_request_error import VivaRequestError


class CustomFlaskRestfulApi(Api):

    def handle_error(self, error):

        if isinstance(error, HTTPException):
            return self._error_response(status_code=error.code, details=error.description)

        if isinstance(error, ConnectionError):
            return self._error_response(status_code=502, details=error.strerror)

        if isinstance(error, VivaRequestError):
            return self._error_response(status_code=error.http_status_code, details=error.message)

        if isinstance(error, MarshmallowValidationError):
            return self._error_response(status_code=400, details=error.messages)

        if not getattr(error, 'message', None):
            return self._error_response(status_code=500, details=f'Server has encountered an unexpected error: {error}')

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
