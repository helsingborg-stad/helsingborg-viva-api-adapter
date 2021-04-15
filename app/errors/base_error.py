class BaseError(Exception):
    def __init__(self, http_status_code: int, *args, **kwargs):
        # If the key `msg` is provided, provide the msg string
        # to Exception class in order to display
        # the msg while raising the exception
        self.http_status_code = http_status_code
        self.kwargs = kwargs
        message = kwargs.get('message')
        if message:
            super().__init__(message)
        self.args = list(args)
        for key in kwargs.keys():
            setattr(self, key, kwargs[key])
