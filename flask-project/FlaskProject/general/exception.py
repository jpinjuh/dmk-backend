class CustomLogException(Exception):
    def __init__(self, exception=None):
        self.exception = exception


class FlaskProjectLogException(Exception):
    def __init__(self, status=None):
        self.status = status

