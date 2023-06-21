from part.constants import (
    SOURCE_AKR,
    SOURCE_ALVADI,
    SOURCE_AMAYAMA,
    SOURCE_BERNARDIPARTS,
    SOURCE_HONDAPARTSNOW,
    SOURCE_HONDASPAREPARTS,
    SOURCE_ONLINETEILE,
)
from part.models import Part, Stock
from rest_framework import serializers


class StockNestedOutputSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stock
        fields = ["id"]


class PartOutputSerializer(serializers.ModelSerializer):
    stock = StockNestedOutputSerializer(many=True, source="stock_set")
    title = serializers.SerializerMethodField()

    class Meta:
        model = Part
        fields = ["reference", "stock", "title"]

    def get_title(self, obj):
        stocks = obj.stock_set.all().values_list("title", "source")
        if not stocks:
            return
        if stocks.filter(source=SOURCE_HONDASPAREPARTS).exists():
            return stocks.get(source=SOURCE_HONDASPAREPARTS)[0]
        elif stocks.filter(source=SOURCE_HONDAPARTSNOW).exists():
            return stocks.get(source=SOURCE_HONDAPARTSNOW)[0]
        elif stocks.filter(source=SOURCE_BERNARDIPARTS).exists():
            return stocks.get(source=SOURCE_BERNARDIPARTS)[0]
        elif stocks.filter(source=SOURCE_AMAYAMA).exists():
            return stocks.get(source=SOURCE_AMAYAMA)[0]
        elif stocks.filter(source=SOURCE_ALVADI).exists():
            return stocks.get(source=SOURCE_ALVADI)[0]
        elif stocks.filter(source=SOURCE_ONLINETEILE).exists():
            return stocks.get(source=SOURCE_ONLINETEILE)[0]
        elif stocks.filter(source=SOURCE_AKR).exists():
            return stocks.get(source=SOURCE_AKR)[0]
        else:
            return stocks[0][0]


class SearchOutputSerializer(serializers.ModelSerializer):
    class Meta:
        model = Part
        fields = ["reference"]


class HistoricalStockNestedOutputSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stock
        fields = ["price", "price_currency", "modified"]
