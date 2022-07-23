import pydantic
from part.part import Part
from contextlib import nullcontext as does_not_raise

from money import Money

import pytest


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
