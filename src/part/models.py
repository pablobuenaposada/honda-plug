from django.contrib.auth.models import User
from django.db import models
from django_countries.fields import CountryField
from django_extensions.db.models import TimeStampedModel
from django_prometheus.models import ExportModelOperationsMixin
from djmoney.models.fields import MoneyField
from simple_history.models import HistoricalRecords

from part.constants import PART_SOURCES, STOCK_SOURCES
from part.managers import PartManager
from part.validators import validate_empty, validate_if_exists, validate_reference


class Part(ExportModelOperationsMixin("part"), TimeStampedModel):
    reference = models.CharField(
        unique=True,
        max_length=15,
        default=None,
        validators=[validate_reference, validate_if_exists],
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

    def get_absolute_url(self):
        """returns the url of the frontend for this part, mainly for sitemap"""
        return f"/part/{self.reference}"

    @property
    def last_time_stock_modified(self):
        """returns the last time a stock of this part was found"""
        if stock := self.stock_set.order_by("-modified").first():
            return stock.modified

    def save(self, **kwargs):
        validate_empty(self.source)
        validate_reference(self.reference)
        if not self.id:
            validate_if_exists(self.reference)
        self.reference = self.reference.upper()
        super().save(**kwargs)

    def __str__(self):
        return self.reference


class Stock(ExportModelOperationsMixin("stock"), TimeStampedModel):
    part = models.ForeignKey(Part, on_delete=models.CASCADE)
    title = models.CharField(max_length=128, db_index=True, blank=True)
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
    # This next field is only added for grafana purposes.
    # Do not update this field manually, it's automated through a signal.
    # To know the last user better to use the historical model that this model has.
    changed_by = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        help_text="Only for grafana purposes",
    )

    history = HistoricalRecords(excluded_fields=["changed_by"])

    class Meta:
        unique_together = ("part", "source", "country")

    def __str__(self):
        return self.part.reference


class Image(ExportModelOperationsMixin("image"), models.Model):
    url = models.URLField(default=None, unique=True, max_length=300)
    stocks = models.ManyToManyField(Stock)

    def save(self, **kwargs):
        validate_empty(self.url)
        super().save(**kwargs)
