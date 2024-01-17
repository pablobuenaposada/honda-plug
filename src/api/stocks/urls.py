from api.stocks.views import StocksBulkCreateView, StocksCreateView, StocksRetrieveView
from django.urls import path

urlpatterns = [
    path("<int:pk>/", StocksRetrieveView.as_view(), name="stocks-detail"),
    path("bulk/", StocksBulkCreateView.as_view(), name="stocks-bulk-create"),
    path("", StocksCreateView.as_view(), name="stocks-create"),
]
