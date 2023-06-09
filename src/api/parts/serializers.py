from part.models import Part, Stock
from rest_framework import serializers


class StockNestedOutputSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stock
        fields = ["id"]


class PartOutputSerializer(serializers.ModelSerializer):
    stock = StockNestedOutputSerializer(many=True, source="stock_set")

    class Meta:
        model = Part
        fields = ["reference", "stock"]
