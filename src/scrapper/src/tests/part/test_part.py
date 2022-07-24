from contextlib import nullcontext as does_not_raise

import pydantic
import pytest
from money import Money

from part.part import Part


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
                    "reference": "foo-bar",
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
                },
                does_not_raise(),
                {
                    "reference": "FOO-BAR-BANANA",
                    "title": "bar",
                    "price": Money(1, "USD"),
                    "image": None,
                    "available": None,
                    "discontinued": None,
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
                },
                does_not_raise(),
                {
                    "reference": "FOO-BAR-BANANA",
                    "title": "bar",
                    "price": Money(1, "USD"),
                    "image": "http://url.com",
                    "available": True,
                    "discontinued": False,
                },
            ),
        ),
    )
    def test_initialization(self, arguments, expectation, result):
        with expectation:
            part = Part(**arguments)
        if result:
            assert part.dict() == result
