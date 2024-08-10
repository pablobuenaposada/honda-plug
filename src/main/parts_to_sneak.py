class PartsToSneak:
    """Singleton class for storing urgent parts to be scraped"""

    _parts = set()

    @classmethod
    def add(cls, reference):
        cls._parts.add(reference)

    @classmethod
    def pop(cls):
        if cls._parts:
            return cls._parts.pop()
