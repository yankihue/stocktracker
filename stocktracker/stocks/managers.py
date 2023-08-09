import requests
from django.db import models


class StockManager(models.Manager):
    """A manager for the Stock model."""

    def populate(self, request):
        """Populates the database with Stock objects."""
        currency1 = "BTC"
        base_currency = "USD"
        url = "https://www.alphavantage.co/query?function=CURRENCY_EXCHANGE_RATE&from_currency={}&to_currency={}&apikey=WX0W0TEMMGW2CVT9".format(
            currency1, base_currency
        )

        observation = requests.get(url=url).json()
        observation = observation["Realtime Currency Exchange Rate"]
        tickerName = observation["1. From_Currency Code"]

        stock = self.get(ticker=tickerName)
        rate = observation["5. Exchange Rate"]
        stock.price = float(rate)
        stock.save()

        return stock
