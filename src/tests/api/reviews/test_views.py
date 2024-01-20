import pytest
from api.reviews.serializers import ReviewPartInputSerializer
from django.contrib.auth.models import Permission, User
from django.shortcuts import resolve_url
from model_bakery import baker
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import ErrorDetail
from review.models import ReviewPart

REFERENCE = "56483-PND-003"


@pytest.mark.django_db
class TestsReviewsCreateView:
    endpoint = resolve_url("api:reviews-create")

    @pytest.fixture(autouse=True)
    def setup_class(self):
        user = baker.make(User)
        user.user_permissions.add(Permission.objects.get(name="Can add review part"))
        self.token = baker.make(Token, user=user)

    def test_url(self):
        assert self.endpoint == "/api/reviews/"

    def test_no_token(self, client):
        response = client.post(
            self.endpoint,
            {"reference": REFERENCE, "source": "foo"},
        )

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_success(self, client):
        assert not ReviewPart.objects.exists()
        response = client.post(
            self.endpoint,
            {"reference": REFERENCE, "source": "foo"},
            HTTP_AUTHORIZATION=f"Token {self.token}",
        )

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data == ReviewPartInputSerializer(ReviewPart.objects.get()).data

    def test_success_already_exists(self, client):
        """
        If review part already exists it should not allow it
        """
        baker.make(ReviewPart, reference=REFERENCE)
        assert ReviewPart.objects.count() == 1

        response = client.post(
            self.endpoint,
            {"reference": REFERENCE, "source": "foo"},
            HTTP_AUTHORIZATION=f"Token {self.token}",
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data == {
            "reference": [
                ErrorDetail(
                    string="review part with this reference already exists.",
                    code="unique",
                )
            ]
        }

    def test_validation_error(self, client):
        response = client.post(
            self.endpoint,
            {},
            HTTP_AUTHORIZATION=f"Token {self.token}",
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data == {
            "reference": [
                ErrorDetail(string="This field is required.", code="required")
            ],
            "source": [ErrorDetail(string="This field is required.", code="required")],
        }
