import json
from .messages import language

class ValidationError(Exception):
    def __init__(self, message=None, error_code=None, **extra):
        msg = message if error_code not in language else language[error_code]
        super().__init__(msg.format(**extra))


class InvalidSchema(Exception):
    def __init__(self, errors: dict):
        self.errors = errors
        super().__init__("Invalid schema: " + json.dumps(errors, default=str, ensure_ascii=False))