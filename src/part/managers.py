from django.db import models
from django.db.models import Count


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
