import functools
from flask import current_app

from app.schemas.response_schema import ResponseSchema
from app.errors.viva_request_error import VivaRequestError


def catch_viva_error(function):

    @functools.wraps(function)
    def wrapper(*args, **kwargs):

        viva_request_response = function(*args, **kwargs)

        response_schema = ResponseSchema()
        validated_viva_request_response = response_schema.load(
            viva_request_response)

        viva_response_status = str(
            validated_viva_request_response['status']).lower()

        if not viva_response_status == 'ok':
            current_app.logger.error(msg={**validated_viva_request_response})
            raise VivaRequestError(
                message={**validated_viva_request_response})

        return validated_viva_request_response

    return wrapper
