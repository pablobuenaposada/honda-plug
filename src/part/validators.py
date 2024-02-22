from django.core.exceptions import ValidationError


def validate_reference(value):
    """
    https://www.vsource.org/VFR-RVF_files/BHondaPartNumbers.htm
    """
    if value == "" or value is None:
        raise ValidationError("empty reference")
    if not (value.replace("-", "").isascii() and value.replace("-", "").isalnum()):
        raise ValidationError("contains non alphanumeric characters apart from hyphens")
    if len(value) > 15:
        raise ValidationError("max 15 chars")
    if not 0 < value.count("-") < 3:
        raise ValidationError("must contain 1 or 2 hyphens")
    if len(value.split("-")[0]) != 5:
        raise ValidationError("must start with 5 characters before first hyphen")
    if len(value.split("-")) == 3 and ("X" in value.upper().split("-")[0]):
        raise ValidationError("can't contain X in first group")
    if len(value.split("-")) == 2 and "X" in value.upper():
        raise ValidationError("can't contain X")


def validate_empty(value):
    if not value:
        raise ValidationError("This field cannot be emtpy")
