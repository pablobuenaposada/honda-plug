from api.parts.views import PartsToScrapView, PartsView, SearchView
from django.urls import path

urlpatterns = [
    path("to-scrap/", PartsToScrapView.as_view(), name="to-scrap"),
    path("<str:reference>/", PartsView.as_view(), name="parts-detail"),
    path("", SearchView.as_view(), name="search"),
]
