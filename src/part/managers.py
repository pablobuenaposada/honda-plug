from datetime import timedelta

from django.db import models
from django.db.models import Case, Count, IntegerField, Value, When
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

    def parts_to_scrap(self):
        """
        Returns all the Parts that had not been delivered to a scraper followed by the ones that been by oldest order
        """
        return (
            super()
            .get_queryset()
            .annotate(
                is_null_last_time_delivered=Case(
                    When(last_time_delivered__isnull=True, then=Value(1)),
                    default=Value(2),
                    output_field=IntegerField(),
                )
            )
            .order_by("is_null_last_time_delivered", "last_time_delivered")
        )
