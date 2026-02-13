from django.core.exceptions import ValidationError


class InvalidStatusChange(ValidationError):
    pass
