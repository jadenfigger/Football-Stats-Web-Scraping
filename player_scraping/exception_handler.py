class APIException(Exception):
    """Custom exception for API errors"""

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class DBException(Exception):
    """Custom exception for Database errors"""

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)
