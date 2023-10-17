from part.models import Image
from rest_framework import serializers


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ["url", "stock", "id"]
        extra_kwargs = {"id": {"read_only": True}, "url": {"required": True}}
