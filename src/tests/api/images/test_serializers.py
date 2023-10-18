import pytest
from api.images.serializers import ImageInputSerializer, ImageOutputSerializer
from model_bakery import baker
from part.constants import SOURCE_TEGIWA
from part.models import Image, Part, Stock
from rest_framework.exceptions import ErrorDetail

REFERENCE = "56483-PND-003"


@pytest.mark.django_db
class TestsImageInputSerializer:
    serializer_class = ImageInputSerializer

    @pytest.fixture(autouse=True)
    def setup_class(self):
        part = baker.make(Part, reference=REFERENCE, source=SOURCE_TEGIWA)
        self.stock = baker.make(Stock, part=part, source=SOURCE_TEGIWA, country="US")

    def test_mandatory(self):
        serializer = self.serializer_class(data={})

        assert not serializer.is_valid()
        assert serializer.errors == {
            "url": [ErrorDetail(string="This field is required.", code="required")],
            "stock": [ErrorDetail(string="This field is required.", code="required")],
        }

    def test_success(self):
        serializer = self.serializer_class(
            data={"stock": self.stock.id, "url": "http://www.foo.com"}
        )

        assert serializer.is_valid()


@pytest.mark.django_db
class TestsImageOutputSerializer:
    serializer_class = ImageOutputSerializer

    @pytest.fixture(autouse=True)
    def setup_class(self):
        part = baker.make(Part, reference=REFERENCE, source=SOURCE_TEGIWA)
        self.stock = baker.make(Stock, part=part, source=SOURCE_TEGIWA, country="US")

    def test_success(self):
        image = baker.make(Image, stocks=[self.stock], url="http://www.foo.com")

        assert self.serializer_class(image).data == {
            "id": image.id,
            "stocks": [self.stock.id],
            "url": image.url,
        }
