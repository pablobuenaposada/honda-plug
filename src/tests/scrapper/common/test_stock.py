from contextlib import nullcontext as does_not_raise

import pydantic
import pytest
from money import Money

from scrapper.common.stock import Stock


class TestPart:
    @pytest.mark.parametrize(
        "arguments, expectation, result",
        (
            (
                {},
                pytest.raises(
                    pydantic.error_wrappers.ValidationError
                ),  # TODO: match regexp
                None,
            ),
            (
                {
                    "reference": "foo",
                    "title": "bar",
                    "price": Money(1, "USD"),
                },
                pytest.raises(pydantic.error_wrappers.ValidationError),
                None,
            ),
            (
                {
                    "reference": "foo-bar-banana-melon",
                    "title": "bar",
                    "price": Money(1, "USD"),
                },
                pytest.raises(pydantic.error_wrappers.ValidationError),
                None,
            ),
            (
                {
                    "reference": "foo-bar-banana",
                    "title": "bar",
                    "price": Money(1, "USD"),
                    "url": "https://www.foo.com",
                },
                does_not_raise(),
                {
                    "reference": "FOO-BAR-BANANA",
                    "title": "bar",
                    "price": Money(1, "USD"),
                    "image": None,
                    "available": None,
                    "discontinued": None,
                    "url": "https://www.foo.com",
                },
            ),
            (
                {
                    "reference": "foo-bar-banana",
                    "title": "bar",
                    "price": Money(1, "USD"),
                    "image": "http://url.com",
                    "available": True,
                    "discontinued": False,
                    "url": "https://www.foo.com",
                },
                does_not_raise(),
                {
                    "reference": "FOO-BAR-BANANA",
                    "title": "bar",
                    "price": Money(1, "USD"),
                    "image": "http://url.com",
                    "available": True,
                    "discontinued": False,
                    "url": "https://www.foo.com",
                },
            ),
        ),
    )
    def test_initialization(self, arguments, expectation, result):
        with expectation:
            part = Stock(**arguments)
        if result:
            assert part.dict() == result
