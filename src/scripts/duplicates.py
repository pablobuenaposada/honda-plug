from django.core.exceptions import MultipleObjectsReturned

from part.models import Part
from scrapper.utils import flatten_reference


def run():
    for part in Part.objects.all():
        print(part)
        regexp = flatten_reference(part.reference)
        regexp = [*regexp]
        regexp = "-?".join(regexp) + "$"

        try:
            Part.objects.get(reference__regex=regexp)
        except MultipleObjectsReturned:
            duplicates = Part.objects.filter(reference__regex=regexp)
            for duplicate in duplicates:
                print(f"{duplicate.id}, {duplicate.reference}")

            print(f"total: {Part.objects.count()}")
            print("which one to keep?")
            id = int(input())
            for duplicate in duplicates:
                if duplicate.id != id:
                    duplicate.delete()
