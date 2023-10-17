from api.images.views import ImagesCreateView
from django.urls import path

urlpatterns = [
    path("", ImagesCreateView.as_view(), name="images-create"),
]
