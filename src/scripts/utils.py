from djmoney.money import Money

from part.models import Image, Part, Stock
from scrapper.part.part import Part as StockParsed


def add_stock(part: Part, stock_found: StockParsed, source: str):
    stock, created = Stock.objects.update_or_create(
        part=part,
        source=source,
        defaults={
            "part": part,
            "title": stock_found.title,
            "price": Money(stock_found.price.amount, stock_found.price.currency),
            "available": stock_found.available,
            "discontinued": stock_found.discontinued,
            "source": source,
            "url": stock_found.url,
        },
    )
    if stock_found.image:
        Image.objects.update_or_create(stock=stock, url=stock_found.image)

    return stock, created
