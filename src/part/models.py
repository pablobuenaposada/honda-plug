from django.db import models
from django_countries.fields import CountryField
from django_extensions.db.models import TimeStampedModel
from django_prometheus.models import ExportModelOperationsMixin
from djmoney.models.fields import MoneyField
from simple_history.models import HistoricalRecords

from part.constants import PART_SOURCES, STOCK_SOURCES
from part.managers import PartManager
from part.tasks import search_for_stocks
from part.validators import validate_empty, validate_reference


class Part(ExportModelOperationsMixin("part"), TimeStampedModel):
    reference = models.CharField(
        unique=True, max_length=15, default=None, validators=[validate_reference]
    )
    source = models.CharField(
        choices=PART_SOURCES,
        max_length=len(max([source[0] for source in PART_SOURCES], key=len)),
    )
    last_time_delivered = models.DateTimeField(
        null=True, help_text="last time when this part has been delivered to a scraper"
    )

    history = HistoricalRecords()
    objects = PartManager()

    def save(self, **kwargs):
        validate_empty(self.source)
        validate_reference(self.reference)
        self.reference = self.reference.upper()
        is_new = self._state.adding
        super().save(**kwargs)
        if is_new:
            # if this is a new Part, let's try to find Stocks for it right away
            search_for_stocks.delay(self.reference)

    def __str__(self):
        return self.reference


class Stock(ExportModelOperationsMixin("stock"), TimeStampedModel):
    part = models.ForeignKey(Part, on_delete=models.CASCADE)
    title = models.CharField(max_length=100, db_index=True)
    price = MoneyField(max_digits=10, null=True, default_currency=None)
    available = models.BooleanField(null=True, default=None)
    discontinued = models.BooleanField(null=True, default=None)
    source = models.CharField(
        choices=STOCK_SOURCES,
        max_length=len(max([source[0] for source in STOCK_SOURCES], key=len)),
        db_index=True,
    )
    quantity = models.IntegerField(null=True, blank=True)
    url = models.URLField()
    country = CountryField()

    history = HistoricalRecords()

    class Meta:
        unique_together = ("part", "source", "country")

    def __str__(self):
        return self.part.reference


class Image(ExportModelOperationsMixin("image"), models.Model):
    url = models.URLField(default=None, unique=True, max_length=300)
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)

    def save(self, **kwargs):
        validate_empty(self.url)
        super().save(**kwargs)
