from api.parts.serializers import HistoricalStockNestedOutputSerializer
from part.models import Stock
from rest_framework import serializers


class StockOutputSerializer(serializers.ModelSerializer):
    history = HistoricalStockNestedOutputSerializer(many=True)

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
        ]
