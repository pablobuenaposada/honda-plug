from api.parts.views import PartsView
from django.urls import path

urlpatterns = [
    path("<str:reference>/", PartsView.as_view(), name="parts-detail"),
]
