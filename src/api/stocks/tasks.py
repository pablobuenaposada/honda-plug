from datetime import datetime

from django_rq import job
from part.models import Part, Stock
from review.models import ReviewPart
from simple_history.utils import bulk_create_with_history, bulk_update_with_history


@job
def bulk_create(serializer):  # noqa: C901
    total_stocks = len(serializer.validated_data)
    parts_not_found = duplicated_stocks = errors = 0

    for stock in serializer.validated_data:
        try:
            part = Part.objects.search_reference(stock["reference"]).get()
        except Part.DoesNotExist:
            try:
                ReviewPart.objects.get_or_create(
                    reference=stock["reference"],
                    defaults={"source": stock["source"]},
                )
            except Exception:
                errors += 1
            else:
                parts_not_found += 1
            stock["part"] = None  # this is what will tell us later to skip it
        else:  # part is found
            try:
                found_stock = Stock.objects.get(
                    part=part, source=stock["source"], country=stock["country"]
                )
                stock["id"] = found_stock.id
                stock["created"] = found_stock.created
                stock["modified"] = datetime.now()
                stock["part"] = part
            except Stock.DoesNotExist:
                stock["part"] = part

        del stock["reference"]

    stocks_seen = set()
    deduplicated_stocks = []

    for stock in serializer.validated_data:
        if stock["part"]:
            if (
                stock["part"].reference,
                stock["country"],
                stock["source"],
            ) not in stocks_seen:
                deduplicated_stocks.append(stock)
                stocks_seen.add(
                    (stock["part"].reference, stock["country"], stock["source"])
                )
            else:
                duplicated_stocks += 1

    stocks_to_update = []
    stocks_to_create = []
    for item in deduplicated_stocks:
        if "id" in item:
            stocks_to_update.append(Stock(**item))
        else:
            stocks_to_create.append(Stock(**item))

    updated_stocks = bulk_update_with_history(
        stocks_to_update,
        Stock,
        [
            "title",
            "price",
            "price_currency",
            "available",
            "discontinued",
            "source",
            "quantity",
            "url",
            "country",
            "modified",
        ],
    )
    created_stocks = bulk_create_with_history(stocks_to_create, Stock)
    assert (
        total_stocks
        == updated_stocks
        + len(created_stocks)
        + duplicated_stocks
        + parts_not_found
        + errors
    )

    return {
        "created": len(created_stocks),
        "duplicated": duplicated_stocks,
        "not_found": parts_not_found,
        "received": total_stocks,
        "updated": updated_stocks,
        "errors": errors,
    }
