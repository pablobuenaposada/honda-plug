import pytest
from django.core.exceptions import ValidationError

from part.validators import validate_reference


class TestValidators:
    @pytest.mark.parametrize(
        "reference, error_message",
        (
            ("", "Empty reference"),
            (None, "Empty reference"),
            ("a", "must contain 1 or 2 hyphens"),
            ("a-b-c-d", "must contain 1 or 2 hyphens"),
            ("14721PRBA00-8", "must start with 5 characters before first hyphen"),
        ),
    )
    def test_validate_reference_fail(self, reference, error_message):
        with pytest.raises(ValidationError) as error:
            validate_reference(reference)
        assert error.value.message == error_message

    @pytest.mark.parametrize(
        "reference",
        ("12210-PZ1-003", "95701-060-5508", "94301-14200", "63915-SEA-300ZZ"),
    )
    def test_validate_reference_success(self, reference):
        validate_reference(reference)
