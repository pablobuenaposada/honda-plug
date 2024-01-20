import pytest
from api.reviews.serializers import ReviewPartInputSerializer
from rest_framework.exceptions import ErrorDetail

REFERENCE = "56483-PND-003"


@pytest.mark.django_db
class TestReviewPartInputSerializer:
    serializer_class = ReviewPartInputSerializer

    def test_mandatory(self):
        serializer = self.serializer_class(data={})

        assert not serializer.is_valid()
        assert serializer.errors == {
            "reference": [
                ErrorDetail(string="This field is required.", code="required")
            ],
            "source": [ErrorDetail(string="This field is required.", code="required")],
        }

    def test_success(self):
        serializer = self.serializer_class(
            data={"reference": REFERENCE, "source": "foo"}
        )

        assert serializer.is_valid()
        assert serializer.validated_data == {"reference": REFERENCE, "source": "foo"}
