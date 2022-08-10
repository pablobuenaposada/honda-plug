from part.models import Part, Stock


def assert_part_main_fields(part, expected):
    for field in {field.name for field in Part._meta.get_fields()} - {
        "modified",
        "created",
        "id",
        "stock",
    }:
        assert getattr(part, field) == expected[field]


def assert_stock_main_fields(stock, expected):
    for field in {field.name for field in Stock._meta.get_fields()} - {
        "price_currency",
        "image",
        "created",
        "id",
        "modified",
        "part",
    }:
        assert getattr(stock, field) == expected[field]
