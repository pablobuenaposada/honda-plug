from api.parts.views import PartsView, SearchView
from django.urls import path

urlpatterns = [
    path("<str:reference>/", PartsView.as_view(), name="parts-detail"),
    path("", SearchView.as_view(), name="search"),
]
