from django.core.cache import cache

CACHE_KEY = "parts_to_sneak"


class PartsToSneak:
    """class for storing urgent parts to be scraped"""

    @classmethod
    def add(cls, reference):
        parts_to_sneak = cache.get(CACHE_KEY, set())
        parts_to_sneak = set(parts_to_sneak)
        parts_to_sneak.add(reference)
        cache.set(CACHE_KEY, parts_to_sneak)

    @classmethod
    def pop(cls):
        parts_to_sneak = cache.get(CACHE_KEY, None)
        if not parts_to_sneak:
            return None
        reference = parts_to_sneak.pop()
        cache.set(CACHE_KEY, parts_to_sneak)
        return reference
