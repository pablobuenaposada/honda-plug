from api.reviews.serializers import ReviewPartInputSerializer
from rest_framework.generics import CreateAPIView
from review.models import ReviewPart


class ReviewsCreateView(CreateAPIView):
    serializer_class = ReviewPartInputSerializer
    queryset = ReviewPart.objects.all()
