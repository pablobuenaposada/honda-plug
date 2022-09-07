from datetime import timedelta

from django.db import models
from django.db.models import Count
from django.utils import timezone


class PartManager(models.Manager):
    def stocked_parts_first(self):
        return (
            super()
            .get_queryset()
            .annotate(num_stocks=Count("stock"))
            .order_by("-num_stocks")
        )

    def stocked_parts_last(self):
        return (
            super()
            .get_queryset()
            .annotate(num_stocks=Count("stock"))
            .order_by("num_stocks")
        )

    def not_updated_since(self, days):
        return (
            super()
            .get_queryset()
            .exclude(stock__modified__gte=timezone.now() - timedelta(days=days))
            .distinct()
        )
