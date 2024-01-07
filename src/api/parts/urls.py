from api.parts.views import PartsToScrapView, PartsView
from django.urls import path

urlpatterns = [
    path("to-scrap/", PartsToScrapView.as_view(), name="to-scrap"),
    path("<str:reference>/", PartsView.as_view(), name="parts-detail"),
]
