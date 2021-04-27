from . import BaseError


class VivaRequestError(BaseError):

    def __init__(self, message):
        super().__init__(http_status_code=503, message=message)
