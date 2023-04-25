import jwt
from flask import request, current_app
from flask_restful import wraps
from werkzeug.exceptions import Unauthorized


def skip_authentication() -> bool:
    return current_app.testing or current_app.debug


def validate_token(token, public_key) -> bool:
    """
    JSON Web Tokens with Public Key Signatures
    https://blog.miguelgrinberg.com/post/json-web-tokens-with-public-key-signatures
    """
    try:
        jwt.decode(token, public_key, algorithms=['RS256'])
        return True
    except Exception as error:
        current_app.logger.debug(msg=error, exc_info=True)
        return False


def authenticate(f):

    @wraps(f)
    def wrapper(*args, **kwargs):
        try:
            is_set_attribute_authenticate = getattr(f, 'authenticate', True)
            will_skip_auth = is_set_attribute_authenticate and skip_authentication()

            if will_skip_auth:
                return f(*args, **kwargs)

            with open(current_app.config['PUBLIC_KEY_FILE']) as public_key_file:
                public_key = public_key_file.read()

            token = request.headers.get('X-Api-Key')

            if not validate_token(token=token, public_key=public_key):
                raise Unauthorized(
                    description='The server could not verify that you are authorized to access the URL requested.')

            return f(*args, **kwargs)

        except Exception as error:
            current_app.logger.debug(msg=error, exc_info=True)
            raise error

    return wrapper
