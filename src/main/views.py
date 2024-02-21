from django.contrib.sitemaps import GenericSitemap
from django.db.models import Count
from django_prometheus import exports
from part.documents import StockDocument
from part.metrics import elasticsearch_stocks, images, parts, stocks, stocks_by_user
from part.models import Image, Part, Stock
from rest_framework.authtoken.models import Token


def prometheus_override_view(request):
    """
    Override the main Prometheus view to include custom metrics
    """
    parts.set(Part.objects.all().count())
    stocks.labels("all").set(Stock.objects.all().count())
    images.set(Image.objects.all().count())
    for source_count in Stock.objects.values("source").annotate(count=Count("source")):
        stocks.labels(source_count["source"]).set(source_count["count"])
    for token in Token.objects.all():
        stocks_by_user.labels(token.user.username).set(
            Stock.objects.filter(changed_by=token.user).count()
        )
    stocks_by_user.labels("empty").set(
        Stock.objects.filter(changed_by__isnull=True).count()
    )
    elasticsearch_stocks.set(StockDocument.search().count())

    return exports.ExportToDjangoView(request)


class PartsSitemap(GenericSitemap):
    limit = 1000
