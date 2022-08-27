import pytest
from django.core.exceptions import ValidationError

from part.validators import validate_reference


class TestValidators:
    @pytest.mark.parametrize(
        "reference, error_message",
        (
            ("", "empty reference"),
            (None, "empty reference"),
            ("?-", "contains non alphanumeric characters apart from hyphens"),
            (" ", "contains non alphanumeric characters apart from hyphens"),
            ("a", "must contain 1 or 2 hyphens"),
            ("a-b-c-d", "must contain 1 or 2 hyphens"),
            ("14721PRBA00-8", "must start with 5 characters before first hyphen"),
            ("12345-12", "second group must be more than 2 characters"),
            ("12345-123-123456", "max 15 chars"),
        ),
    )
    def test_validate_reference_fail(self, reference, error_message):
        with pytest.raises(ValidationError) as error:
            validate_reference(reference)
        assert error.value.message == error_message

    @pytest.mark.parametrize(
        "reference",
        (
            "12210-PZ1-003",
            "95701-060-5508",
            "94301-14200",
            "93891-0501007",
            "63915-SEA-300ZZ",
        ),
    )
    def test_validate_reference_success(self, reference):
        validate_reference(reference)
