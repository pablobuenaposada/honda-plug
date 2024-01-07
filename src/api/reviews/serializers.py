from rest_framework import serializers
from review.models import ReviewPart


class ReviewPartInputSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReviewPart
        fields = ["reference"]
