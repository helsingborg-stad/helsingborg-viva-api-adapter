import jwt
from flask import request, current_app
from flask_restful import wraps
from werkzeug.exceptions import Unauthorized
from werkzeug.exceptions import BadRequest


def validate_token() -> bool:
    """
    JSON Web Tokens with Public Key Signatures
    https://blog.miguelgrinberg.com/post/json-web-tokens-with-public-key-signatures
    """
    try:
        if 'X-API-Key' not in request.headers:
            raise BadRequest(description='Header X-API-Key missing!')

        token = request.headers['X-Api-Key']

        if current_app.config['ENV'] in ('development', 'test'):
            public_key = open('jwtRS256_dev.key.pub').read()
        else:
            public_key = open('jwtRS256.key.pub').read()

        jwt.decode(token, public_key, algorithms=['RS256'])

        return True

    except Exception as error:
        current_app.logger.debug(msg=error, exc_info=True)
        return False


def authenticate(f):
    """
    Decorator function to validate token on route resources

    Example:
    class Applications(Resource):
        method_decorators = [authenticate]
        ...
        ...
    """
    @wraps(f)
    def wrapper(*args, **kwargs):
        if not getattr(f, 'authenticate', True):
            return f(*args, **kwargs)

        if not validate_token():
            raise Unauthorized(
                description='The server could not verify that you are authorized to access the URL requested.')

        return f(*args, **kwargs)

    return wrapper
