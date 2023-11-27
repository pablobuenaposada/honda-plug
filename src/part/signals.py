from django.db.models import signals
from django.db.models.signals import post_save
from django.dispatch import receiver

from part.models import Stock


@receiver(post_save, sender=Stock)
def post_save_stock(sender, instance, **kwargs):
    signals.post_save.disconnect(post_save_stock, sender=Stock)
    try:
        instance.changed_by = instance.history.first().history_user
    except AttributeError:
        instance.changed_by = None
    instance.save_without_historical_record(update_fields=["changed_by"])
    signals.post_save.connect(post_save_stock, sender=Stock)
