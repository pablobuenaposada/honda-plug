from api.stocks.serializers import StockOutputSerializer
from part.models import Stock
from rest_framework.generics import RetrieveAPIView


class StocksView(RetrieveAPIView):
    serializer_class = StockOutputSerializer
    queryset = Stock.objects.all()
