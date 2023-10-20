from django.apps import AppConfig


class PartConfig(AppConfig):
    name = "part"

    def ready(self):
        import part.signals  # noqa: F401
