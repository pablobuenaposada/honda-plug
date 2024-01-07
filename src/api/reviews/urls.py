from api.reviews.views import ReviewsCreateView
from django.urls import path

urlpatterns = [
    path("", ReviewsCreateView.as_view(), name="reviews-create"),
]
