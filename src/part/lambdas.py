from part.models import Part


def add_part(reference, source):
    Part.objects.create(reference=reference, source=source)
