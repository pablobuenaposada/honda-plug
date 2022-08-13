import pydantic
import pytest
from money import Money

from part.constants import SOURCE_AMAYAMA
from scrapper.common.stock import Stock


class TestStock:
    @pytest.mark.parametrize(
        "arguments, expected",
        (
            (
                {},
                "4 validation errors for Stock\nreference\n  field required (type=value_error.missing)\nurl\n  field required (type=value_error.missing)\nsource\n  field required (type=value_error.missing)\ncountry\n  field required (type=value_error.missing)",
            ),
            (
                {"reference": "foo", "url": "https://www.foo.com", "country": "us"},
                "2 validation errors for Stock\nreference\n  must contain 2 or 3 times character - (type=value_error)\nsource\n  field required (type=value_error.missing)",
            ),
            (
                {
                    "reference": "foo-bar-banana-melon",
                    "url": "https://www.foo.com",
                    "country": "us",
                },
                "2 validation errors for Stock\nreference\n  must contain 2 or 3 times character - (type=value_error)\nsource\n  field required (type=value_error.missing)",
            ),
        ),
    )
    def test_fail(self, arguments, expected):
        with pytest.raises(pydantic.error_wrappers.ValidationError) as error:
            Stock(**arguments)
        assert str(error.value) == expected

    @pytest.mark.parametrize(
        "arguments, result",
        (
            (
                {
                    "reference": "FOO-BAR-BANANA",
                    "url": "https://www.foo.com",
                    "country": "us",
                    "source": SOURCE_AMAYAMA,
                },
                {
                    "reference": "FOO-BAR-BANANA",
                    "url": "https://www.foo.com",
                    "country": "us",
                    "source": SOURCE_AMAYAMA,
                    "title": None,
                    "price": None,
                    "image": None,
                    "available": None,
                    "discontinued": None,
                    "quantity": None,
                },
            ),  # minimal fields
            (
                {
                    "reference": "foo-bar-banana",
                    "title": "bar",
                    "country": "us",
                    "source": SOURCE_AMAYAMA,
                    "price": Money(1, "USD"),
                    "image": "http://url.com",
                    "available": True,
                    "discontinued": False,
                    "url": "https://www.foo.com",
                },
                {
                    "reference": "FOO-BAR-BANANA",
                    "title": "bar",
                    "country": "us",
                    "source": SOURCE_AMAYAMA,
                    "price": Money(1, "USD"),
                    "image": "http://url.com",
                    "available": True,
                    "discontinued": False,
                    "url": "https://www.foo.com",
                    "quantity": None,
                },
            ),  # all the fields
        ),
    )
    def test_success(self, arguments, result):
        part = Stock(**arguments)
        assert part.dict() == result
