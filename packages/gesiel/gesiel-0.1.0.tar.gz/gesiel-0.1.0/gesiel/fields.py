from .messages import Messages
from .exceptions import ValidationError
import math
class Field:
    def __init__(self, default=None, required=False, strict=False, validators=[]):
        self.default = default
        self.required = required
        self.strict = strict
        self.validators = validators

    def validate(self, value):
        errors = []
        for validator in self.validators:
            try:
                validator(value)
            except ValidationError as error:
                errors.append(error)
        return errors
    
    def load(self, value):
        return value

class String(Field):
    def load(self, value):
        if isinstance(value, str):
            return value
        elif self.strict and not isinstance(value, (int, float)):
            raise ValidationError(error_code=Messages.MUST_BE_STRING)
        return str(value)

class Bool(Field):
    def load(self, value):
        if isinstance(value, bool):
            return value
        raise ValidationError(error_code=Messages.MUST_BE_BOOLEAN)

class Int(Field):
    def load(self, value):
        if isinstance(value, int):
            return value
        elif self.strict and not isinstance(value, (str, float)):
            raise ValidationError(error_code=Messages.MUST_BE_INTEGER)
        try:
            return int(value)
        except ValueError:
            raise ValidationError(error_code=Messages.MUST_BE_INTEGER)
