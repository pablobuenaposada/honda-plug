from django.core.exceptions import ValidationError
from django.db import models
from django_extensions.db.models import TimeStampedModel
from djmoney.models.fields import MoneyField
from simple_history.models import HistoricalRecords

from part.constants import PART_SOURCES, STOCK_SOURCES
from part.validators import validate_empty, validate_reference


class Part(TimeStampedModel):
    reference = models.CharField(
        unique=True, max_length=15, default=None, validators=[validate_reference]
    )
    source = models.CharField(choices=PART_SOURCES, max_length=20)

    history = HistoricalRecords()

    def save(self, **kwargs):
        validate_empty(self.source)
        validate_reference(self.reference)
        self.reference = self.reference.upper()
        super().save(**kwargs)

    def __str__(self):
        return self.reference


class Stock(TimeStampedModel):
    part = models.ForeignKey(Part, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    price = MoneyField(max_digits=10, null=True, default_currency=None)
    available = models.BooleanField(null=True, default=None)
    discontinued = models.BooleanField(null=True, default=None)
    source = models.CharField(choices=STOCK_SOURCES, max_length=20)
    quantity = models.IntegerField(null=True, blank=True)
    url = models.URLField()

    history = HistoricalRecords()

    class Meta:
        unique_together = ("part", "source")

    def __str__(self):
        return self.part.reference


class Image(models.Model):
    url = models.URLField(default=None, unique=True)
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)

    def save(self, **kwargs):
        validate_empty(self.url)
        super().save(**kwargs)
