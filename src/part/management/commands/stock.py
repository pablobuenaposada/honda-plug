from django.core.management.base import BaseCommand

from part.models import Part
from part.tasks import enqueue_queryset


class Command(BaseCommand):
    help = "enqueues stock to be updated"

    def add_arguments(self, parser):
        parser.add_argument("days", type=int)

    def handle(self, *args, **options):
        qs = Part.objects.not_updated_since(options["days"])[:3000]
        enqueue_queryset.delay(qs, at_front=True)
