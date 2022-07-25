from django.core.exceptions import ValidationError
from django.db import models
from django_extensions.db.models import TimeStampedModel


class Part(TimeStampedModel):
    reference = models.CharField(unique=True, max_length=13, default=None)

    def save(self, **kwargs):
        if self.reference == "":
            raise ValidationError("Empty reference")
        super().save(**kwargs)


class Stock(TimeStampedModel):
    reference = models.ForeignKey(Part, on_delete=models.CASCADE)
    title = models.CharField(max_length=20)
