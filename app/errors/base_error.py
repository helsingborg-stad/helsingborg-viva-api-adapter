class BaseError(Exception):
    def __init__(self, http_status_code: int, *args, **kwargs):
        self.http_status_code = http_status_code
        self.kwargs = kwargs
        message = kwargs.get('message')
        if message:
            super().__init__(message)
        self.args = tuple(args)
        for key in kwargs.keys():
            setattr(self, key, kwargs[key])
