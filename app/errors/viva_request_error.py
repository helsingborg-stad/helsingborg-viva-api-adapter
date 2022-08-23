from app.errors.base_error import BaseError


class VivaRequestError(BaseError):

    def __init__(self, message):
        self.message = message
        super().__init__(http_status_code=503, message=self.message)
