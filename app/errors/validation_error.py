from app.errors.base_error import BaseError


class CustomValidationError(BaseError):

    def __init__(self, message):
        super().__init__(http_status_code=400, message=message)
