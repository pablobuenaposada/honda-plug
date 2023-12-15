"""main URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.sitemaps import GenericSitemap
from django.contrib.sitemaps.views import sitemap
from django.urls import include, path
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
)
from part.models import Part

from main.views import prometheus_override_view


def trigger_error(request):
    return 1 / 0


info_dict = {
    "queryset": Part.objects.all(),
    "date_field": "last_time_stock_modified",
}

urlpatterns = [
    path("admin/", admin.site.urls),
    path("sentry-debug/", trigger_error),
    path("metrics", prometheus_override_view, name="prometheus-django-metrics"),
    path("api/", include("api.urls", namespace="api")),
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/docs/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),
    path(
        "sitemap.xml",
        sitemap,
        {"sitemaps": {"part": GenericSitemap(info_dict)}},
        name="django.contrib.sitemaps.views.sitemap",
    ),
]
