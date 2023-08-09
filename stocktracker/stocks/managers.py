import datetime
import time

import requests
from django.db import models


class StockManager(models.Manager):
    """A manager for the Stock model."""

    def populate(self, stock):
        """Populates the database with Stock objects."""
        currency = stock.ticker
        base_currency = "USD"  # always compare against USD price
        url = "https://www.alphavantage.co/query?function=CURRENCY_EXCHANGE_RATE&from_currency={}&to_currency={}&apikey=WX0W0TEMMGW2CVT9".format(
            currency, base_currency
        )

        observation = requests.get(url=url).json()
        try:
            observation["Realtime Currency Exchange Rate"]
        except KeyError:  # means we hit API limit
            return None

        rate = observation["Realtime Currency Exchange Rate"]["5. Exchange Rate"]
        timestamp = datetime.datetime.now()
        stock.price = float(rate)
        stock.datetime = timestamp
        stock.save()

        return self
