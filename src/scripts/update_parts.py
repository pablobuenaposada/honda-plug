from part.models import Part
from part.tasks import search_for_stocks


def run(*args):
    """
    run: python src/manage.py runscript update_parts --script-args 100
    first argument is how many days since the part has not received an update of stock
    """
    for part in Part.objects.not_updated_since(int(args[0])).iterator():
        search_for_stocks.delay(part.reference)
