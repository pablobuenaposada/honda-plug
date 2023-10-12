from api.stocks.serializers import StockInputSerializer, StockOutputSerializer
from drf_spectacular.utils import extend_schema
from part.models import Stock
from rest_framework import status
from rest_framework.exceptions import ErrorDetail, ValidationError
from rest_framework.generics import CreateAPIView, RetrieveAPIView
from rest_framework.response import Response


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
