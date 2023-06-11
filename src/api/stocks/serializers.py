from api.parts.serializers import HistoricalStockNestedOutputSerializer
from part.models import Image, Stock
from rest_framework import serializers


class ImageNestedOutputSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ["url"]


class StockOutputSerializer(serializers.ModelSerializer):
    history = HistoricalStockNestedOutputSerializer(many=True)
    images = ImageNestedOutputSerializer(many=True, source="image_set")

    class Meta:
        model = Stock
        fields = [
            "id",
            "title",
            "price",
            "price_currency",
            "available",
            "discontinued",
            "source",
            "quantity",
            "url",
            "country",
            "history",
            "images",
        ]
