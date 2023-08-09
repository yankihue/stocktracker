import requests
from django.conf import settings
from django.db import models
from django.utils import timezone

from stocktracker.stocks.models import Stock


class StockManager(models.Manager):
    """A class containing methods for getting the weather data required for
    each job using the OpenWeather API."""

    def populate(self, job):
        """Populates the database with Stock objects."""
        currency1 = "BTC"
        currency2 = "USD"
        url = "https://www.alphavantage.co/query?function=CURRENCY_EXCHANGE_RATE&from_currency={}&to_currency={}&apikey=WX0W0TEMMGW2CVT9".format(
            currency1, currency2
        )

        observation = requests.get(url=url).json()
        tickerName = observation["Realtime Currency Exchange Rate"][
            "1. From_Currency Code"
        ]
        # x = Stock.objects.filter(ticker=tickerName)

        stock = Stock.objects.get(ticker=tickerName)
        stock.price = float(
            observation["Realtime Currency Exchange Rate"]["5. Exchange Rate"]
        )
        stock.save()

        return stock
