from django_elasticsearch_dsl_drf.serializers import DocumentSerializer
from part.constants import (
    SOURCE_AKR,
    SOURCE_ALVADI,
    SOURCE_AMAYAMA,
    SOURCE_BERNARDIPARTS,
    SOURCE_HONDAPARTSNOW,
    SOURCE_HONDASPAREPARTS,
    SOURCE_ONLINETEILE,
)
from part.documents import StockDocument
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
        fields = ["id", "reference", "stock", "title", "last_time_delivered"]

    def get_title(self, obj):
        stocks = obj.stock_set.all().values_list("title", "source")
        if not stocks:
            return
        if stocks.filter(source=SOURCE_HONDASPAREPARTS).exists():
            return stocks.filter(source=SOURCE_HONDASPAREPARTS).first()[0]
        elif stocks.filter(source=SOURCE_HONDAPARTSNOW).exists():
            return stocks.filter(source=SOURCE_HONDAPARTSNOW).first()[0]
        elif stocks.filter(source=SOURCE_BERNARDIPARTS).exists():
            return stocks.filter(source=SOURCE_BERNARDIPARTS).first()[0]
        elif stocks.filter(source=SOURCE_AMAYAMA).exists():
            return stocks.filter(source=SOURCE_AMAYAMA).first()[0]
        elif stocks.filter(source=SOURCE_ALVADI).exists():
            return stocks.filter(source=SOURCE_ALVADI).first()[0]
        elif stocks.filter(source=SOURCE_ONLINETEILE).exists():
            return stocks.filter(source=SOURCE_ONLINETEILE).first()[0]
        elif stocks.filter(source=SOURCE_AKR).exists():
            return stocks.filter(source=SOURCE_AKR).first()[0]
        else:
            return stocks.first()[0]


class HistoricalStockNestedOutputSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stock
        fields = ["price", "price_currency", "modified"]


class StockDocumentSerializer(DocumentSerializer):
    class Meta:
        document = StockDocument
        fields = ("title", "part")
