from django_prometheus import exports

from part.metrics import images, parts, stocks
from part.models import Image, Part, Stock


def prometheus_override_view(request):
    """
    Override the main Prometheus view to update custom metrics
    """
    parts.set(Part.objects.all().count())
    stocks.set(Stock.objects.all().count())
    images.set(Image.objects.all().count())

    return exports.ExportToDjangoView(request)
