from api.stocks.views import StocksCreateView, StocksRetrieveView
from django.urls import path

urlpatterns = [
    path("<int:pk>/", StocksRetrieveView.as_view(), name="stocks-detail"),
    path("", StocksCreateView.as_view(), name="stocks-create"),
]
