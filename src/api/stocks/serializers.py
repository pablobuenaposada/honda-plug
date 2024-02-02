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


class StockInputSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stock
        fields = [
            "part",
            "title",
            "price",
            "price_currency",
            "available",
            "discontinued",
            "source",
            "quantity",
            "url",
            "country",
        ]


class StockBulkInputSerializer(StockInputSerializer):
    reference = serializers.CharField()

    class Meta:
        model = Stock
        fields = [
            field for field in StockInputSerializer.Meta.fields if field != "part"
        ] + ["reference"]

    def to_internal_value(self, data):
        try:
            return super().to_internal_value(data)
        except serializers.ValidationError as e:
            # if an error is found we attach the reference field too, so we can debug
            e.detail.setdefault("reference", data.get("reference"))
            raise e
