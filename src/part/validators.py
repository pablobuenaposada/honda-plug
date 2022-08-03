from django.core.exceptions import ValidationError


def validate_reference(value):
    if value == "" or value is None:
        raise ValidationError("Empty reference")
    if not 0 < value.count("-") < 3:
        raise ValidationError("must contain 2 or 3 times character -")


def validate_empty(value):
    if not value:
        raise ValidationError("This field cannot be emtpy")
