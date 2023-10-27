from django_prometheus import exports
from part.constants import STOCK_SOURCES
from part.metrics import images, parts, stocks, stocks_by_user
from part.models import Image, Part, Stock
from rest_framework.authtoken.models import Token


def prometheus_override_view(request):
    """
    Override the main Prometheus view to include custom metrics
    """
    parts.set(Part.objects.all().count())
    stocks.labels("all").set(Stock.objects.all().count())
    images.set(Image.objects.all().count())
    for source in STOCK_SOURCES:
        stocks.labels(source[0]).set(Stock.objects.filter(source=source[0]).count())
    for token in Token.objects.all():
        stocks_by_user.labels(token.user.username).set(
            Stock.objects.filter(changed_by=token.user).count()
        )
    stocks_by_user.labels("empty").set(
        Stock.objects.filter(changed_by__isnull=True).count()
    )

    return exports.ExportToDjangoView(request)
