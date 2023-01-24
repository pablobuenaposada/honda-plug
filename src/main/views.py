from django_prometheus import exports

from part.constants import STOCK_SOURCES
from part.metrics import images, parts, stocks
from part.models import Image, Part, Stock


def prometheus_override_view(request):
    """
    Override the main Prometheus view to include custom metrics
    """
    parts.set(Part.objects.all().count())
    stocks.labels("all").set(Stock.objects.all().count())
    images.set(Image.objects.all().count())
    for source in STOCK_SOURCES:
        stocks.labels(source[0]).set(Stock.objects.filter(source=source[0]).count())

    return exports.ExportToDjangoView(request)
