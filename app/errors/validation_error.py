from . import BaseError


class ValidationError(BaseError):
    """ Should be raised in case of custom validation """

    def __init__(self, message):
        super().__init__(http_status_code=400, message=message)
