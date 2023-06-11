from api.stocks.views import StocksView
from django.urls import path

urlpatterns = [
    path("<int:pk>/", StocksView.as_view(), name="stocks-detail"),
]
