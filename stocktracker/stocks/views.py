import requests
from django.contrib.auth.models import Group, User
from rest_framework import generics, permissions, viewsets
from rest_framework.mixins import ListModelMixin
from rest_framework.response import Response
from rest_framework.views import APIView
from stocks.models import Stock
from stocks.serializers import GroupSerializer, StockSerializer, UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """

    queryset = User.objects.all().order_by("-date_joined")
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """

    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]


# class StocksViewSet(viewsets.ModelViewSet):
#     """
#     API endpoint that allows stocks to be viewed.
#     """

#     queryset = Stock.objects.all()
#     serializer_class = StockSerializer
#     permission_classes = [permissions.IsAuthenticated]


class StockList(ListModelMixin, generics.GenericAPIView):
    """
    List all snippets, or create a new snippet.
    """

    queryset = Stock.objects.all()
    serializer_class = StockSerializer(queryset, many=True)

    def get(self, request, format=None):
        # return Response(serializer.data)
        currency1 = "BTC"
        currency2 = "USD"
        url = "https://www.alphavantage.co/query?function=CURRENCY_EXCHANGE_RATE&from_currency={}&to_currency={}&apikey=WX0W0TEMMGW2CVT9".format(
            currency1, currency2
        )

        observation = requests.get(url=url).json()
        ticker = observation["Realtime Currency Exchange Rate"]["1. From_Currency Code"]
        tickerName = observation["Realtime Currency Exchange Rate"][
            "2. From_Currency Name"
        ]
        exchangeRate = observation["Realtime Currency Exchange Rate"][
            "5. Exchange Rate"
        ]
        if Stock.objects.filter(ticker=ticker).exists():
            stock = Stock.objects.get(ticker=ticker)
            stock.price = exchangeRate
            stock.save()
        print(tickerName)
        return Response(observation)
