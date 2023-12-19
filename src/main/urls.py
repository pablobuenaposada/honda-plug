from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.urls import include, path
from django.views.decorators.cache import cache_page
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
)
from part.models import Part

from main.views import PartsSitemap, prometheus_override_view

SITEMAP_CACHE_SECONDS = 60 * 60


def trigger_error(request):
    return 1 / 0


urlpatterns = [
    path("admin/", admin.site.urls),
    path("sentry-debug/", trigger_error),
    path("metrics", prometheus_override_view, name="prometheus-django-metrics"),
    path("api/", include("api.urls", namespace="api")),
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/docs/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),
    path(
        "sitemap.xml",
        cache_page(SITEMAP_CACHE_SECONDS)(sitemap),
        {
            "sitemaps": {
                "part": PartsSitemap(
                    {
                        "queryset": Part.objects.all(),
                        "date_field": "last_time_stock_modified",
                    },
                    protocol="https",
                )
            }
        },
        name="django.contrib.sitemaps.views.sitemap",
    ),
]
