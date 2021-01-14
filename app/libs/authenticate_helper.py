import jwt
from flask import request
from flask_restful import abort, wraps


def validate_token():
    if 'X-API-Key' not in request.headers:
        return False

    token = request.headers['X-Api-Key']
    public_key = open('jwtRS256.key.pub').read()

    try:
        jwt.decode(token, public_key, algorithms=['RS256'])
    except Exception:
        return False

    return True


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
            abort(http_status_code=401, message='Unauthorized')

        return f(*args, **kwargs)

    return wrapper
