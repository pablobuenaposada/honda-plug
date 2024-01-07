from django.db import models
from django_extensions.db.models import TimeStampedModel


class ReviewPart(TimeStampedModel):
    reference = models.CharField(unique=True, max_length=30)
