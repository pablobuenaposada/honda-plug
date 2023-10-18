from part.models import Image, Stock
from rest_framework import serializers


class ImageOutputSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ["id", "url", "stocks"]


class ImageInputSerializer(serializers.ModelSerializer):
    stock = serializers.PrimaryKeyRelatedField(queryset=Stock.objects.all())

    class Meta:
        model = Image
        fields = ["url", "stock"]
        extra_kwargs = {"url": {"required": True}}
