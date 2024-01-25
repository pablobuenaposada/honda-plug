from datetime import datetime

from api.stocks.serializers import (
    StockBulkInputSerializer,
    StockBulkOutputSerializer,
    StockInputSerializer,
    StockOutputSerializer,
)
from drf_spectacular.utils import extend_schema
from part.models import Part, Stock
from rest_framework import status
from rest_framework.exceptions import ErrorDetail, ValidationError
from rest_framework.generics import CreateAPIView, RetrieveAPIView
from rest_framework.response import Response
from review.models import ReviewPart
from simple_history.utils import bulk_create_with_history, bulk_update_with_history


class StocksRetrieveView(RetrieveAPIView):
    permission_classes = []
    serializer_class = StockOutputSerializer
    queryset = Stock.objects.all()


class StocksCreateView(CreateAPIView):
    serializer_class = StockOutputSerializer
    queryset = Stock.objects.all()

    @extend_schema(request=StockInputSerializer)
    def post(self, request, *args, **kwargs):
        serializer_class = StockInputSerializer
        serializer = serializer_class(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except ValidationError as e:
            if e.args == (
                {
                    "non_field_errors": [
                        ErrorDetail(
                            string="The fields part, source, country must make a unique set.",
                            code="unique",
                        )
                    ]
                },
            ):
                # this validation error is a special case where the stock already exists,
                # so it's just about finding the instance and updating it
                instance = Stock.objects.get(
                    part=serializer.data["part"],
                    source=serializer.data["source"],
                    country=serializer.data["country"],
                )
                serializer = serializer_class(instance, data=request.data)
                serializer.is_valid(raise_exception=True)
            else:
                raise e
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            self.get_serializer(serializer.instance).data,
            status=status.HTTP_201_CREATED,
            headers=headers,
        )


@extend_schema(request=StockBulkInputSerializer)
class StocksBulkCreateView(CreateAPIView):
    """
    Allows the creation of multiple stocks in one call.
    If there's any validation error the entire bulk would be discarded,
    duplicated stocks by reference, country and source would be skipped only using the first entry.
    """

    queryset = Stock.objects.all()
    serializer_class = StockBulkOutputSerializer

    def perform_create(self, serializer):  # noqa: C901
        total_stocks = len(serializer.validated_data)
        parts_not_found = duplicated_stocks = 0
        errors = 0

        for stock in serializer.validated_data:
            try:
                part = Part.objects.search_reference(stock["reference"]).get()
            except Part.DoesNotExist:
                try:
                    ReviewPart.objects.get_or_create(
                        reference=stock["reference"],
                        defaults={"source": stock["source"]},
                    )
                except Exception:
                    errors += 1
                else:
                    parts_not_found += 1
                stock["part"] = None  # this is what will tell us later to skip it
            else:  # part is found
                try:
                    found_stock = Stock.objects.get(
                        part=part, source=stock["source"], country=stock["country"]
                    )
                    stock["id"] = found_stock.id
                    stock["created"] = found_stock.created
                    stock["modified"] = datetime.now()
                    stock["part"] = part
                except Stock.DoesNotExist:
                    stock["part"] = part

            del stock["reference"]

        stocks_seen = set()
        deduplicated_stocks = []

        for stock in serializer.validated_data:
            if stock["part"]:
                if (
                    stock["part"].reference,
                    stock["country"],
                    stock["source"],
                ) not in stocks_seen:
                    deduplicated_stocks.append(stock)
                    stocks_seen.add(
                        (stock["part"].reference, stock["country"], stock["source"])
                    )
                else:
                    duplicated_stocks += 1

        stocks_to_update = []
        stocks_to_create = []
        for item in deduplicated_stocks:
            if "id" in item:
                stocks_to_update.append(Stock(**item))
            else:
                stocks_to_create.append(Stock(**item))

        updated_stocks = bulk_update_with_history(
            stocks_to_update,
            Stock,
            [
                "title",
                "price",
                "price_currency",
                "available",
                "discontinued",
                "source",
                "quantity",
                "url",
                "country",
                "modified",
            ],
        )
        created_stocks = bulk_create_with_history(stocks_to_create, Stock)
        assert (
            total_stocks
            == updated_stocks
            + len(created_stocks)
            + duplicated_stocks
            + parts_not_found
            + errors
        )
        serializer = self.serializer_class(
            data={
                "created": len(created_stocks),
                "duplicated": duplicated_stocks,
                "not_found": parts_not_found,
                "received": total_stocks,
                "updated": updated_stocks,
                "errors": errors,
            }
        )
        serializer.is_valid(raise_exception=True)

        return serializer

    def create(self, request, *args, **kwargs):
        serializer = StockBulkInputSerializer(data=request.data, many=True)
        serializer.is_valid(raise_exception=True)
        output_serializer = self.perform_create(serializer)
        headers = self.get_success_headers(output_serializer.data)
        return Response(
            output_serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )
