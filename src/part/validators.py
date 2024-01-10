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
    if len(value.split("-")[1]) < 3:
        raise ValidationError("second group must be more than 2 characters")


def validate_empty(value):
    if not value:
        raise ValidationError("This field cannot be emtpy")


def validate_if_exists(value):
    """check if the reference but normalized already exists"""
    from part.models import Part

    if Part.objects.search_reference(value):
        raise ValidationError(
            f"The normalized reference '{value.replace('-', '')}' already exists."
        )
