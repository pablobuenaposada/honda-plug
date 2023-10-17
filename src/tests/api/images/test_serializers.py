import pytest
from api.images.serializers import ImageSerializer
from model_bakery import baker
from part.constants import SOURCE_TEGIWA
from part.models import Image, Part, Stock
from rest_framework.exceptions import ErrorDetail

REFERENCE = "56483-PND-003"


@pytest.mark.django_db
class TestsImageSerializer:
    serializer_class = ImageSerializer

    @pytest.fixture(autouse=True)
    def setup_class(self):
        part = baker.make(Part, reference=REFERENCE, source=SOURCE_TEGIWA)
        self.stock = baker.make(Stock, part=part, source=SOURCE_TEGIWA, country="US")

    def test_mandatory(self):
        serializer = self.serializer_class(data={})

        assert not serializer.is_valid()
        assert serializer.errors == {
            "stock": [ErrorDetail(string="This field is required.", code="required")],
            "url": [ErrorDetail(string="This field is required.", code="required")],
        }

    def test_success_input(self):
        serializer = self.serializer_class(
            data={"stock": self.stock.id, "url": "http://www.foo.com"}
        )

        assert serializer.is_valid()
        assert serializer.save()

    def test_success_output(self):
        image = baker.make(Image, stock=self.stock, url="http://www.foo.com")

        assert self.serializer_class(image).data == {
            "id": image.id,
            "stock": self.stock.id,
            "url": image.url,
        }
