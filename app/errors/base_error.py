class BaseError(Exception):
    def __init__(self, http_status_code: int, *args, **kwargs):
        # If the key `msg` is provided, provide the msg string
        # to Exception class in order to display
        # the msg while raising the exception
        self.http_status_code = http_status_code
        self.kwargs = kwargs
        msg = kwargs.get('msg', kwargs.get('message'))
        if msg:
            args = (msg,)
            super().__init__(args)
        self.args = list(args)
        for key in kwargs.keys():
            setattr(self, key, kwargs[key])
