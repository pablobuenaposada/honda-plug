from django.core.exceptions import ValidationError


def validate_reference(value):
    if value == "" or value is None:
        raise ValidationError("Empty reference")
    if not 0 < value.count("-") < 3:
        raise ValidationError("must contain 1 or 2 hyphens")
    if len(value.split("-")[0]) != 5:
        raise ValidationError("must start with 5 characters before first hyphen")


def validate_empty(value):
    if not value:
        raise ValidationError("This field cannot be emtpy")
