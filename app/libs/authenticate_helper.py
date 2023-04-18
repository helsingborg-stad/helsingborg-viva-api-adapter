import jwt
from flask import request, current_app
from flask_restful import wraps
from werkzeug.exceptions import Unauthorized


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
            is_testing = current_app.testing
            is_attribute_authenticate = getattr(f, 'authenticate', True)

            if not is_attribute_authenticate or is_testing:
                return f(*args, **kwargs)

            public_key_file = current_app.config['PUBLIC_KEY_FILE']
            public_key = open(public_key_file).read()

            if not validate_token(token=request.headers['X-Api-Key'],
                                  public_key=public_key):
                raise Unauthorized(
                    description='The server could not verify that you are authorized to access the URL requested.')

            return f(*args, **kwargs)

        except Exception as error:
            current_app.logger.debug(msg=error, exc_info=True)
            raise error

    return wrapper
