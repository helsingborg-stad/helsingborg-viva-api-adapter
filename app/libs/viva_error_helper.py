import functools

from ..schemas import ResponseSchema
from ..errors import VivaRequestError


def catch_viva_error(function):

    @functools.wraps(function)
    def wrapper(*args, **kwargs):

        viva_request_response = function(*args, **kwargs)

        response_schema = ResponseSchema()
        validated_viva_request_response = response_schema.load(
            viva_request_response)

        if not validated_viva_request_response['status'] == 'ok':
            raise VivaRequestError(
                message={**validated_viva_request_response})

        return validated_viva_request_response

    return wrapper
