from django.contrib import admin
from django.contrib.sitemaps import views as sitemaps_views
from django.urls import include, path
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
)
from part.models import Part

from main.views import PartsSitemap, prometheus_override_view


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
        sitemaps_views.index,
        {
            "sitemaps": {
                "parts": PartsSitemap(
                    {"queryset": Part.objects.all()}, protocol="https"
                )
            }
        },
        name="django.contrib.sitemaps.views.index",
    ),
    path(
        "sitemap-<section>.xml",
        sitemaps_views.sitemap,
        {
            "sitemaps": {
                "parts": PartsSitemap(
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
