import datetime
import time

import requests
from django.db import models


class StockManager(models.Manager):
    """A manager for the Stock model."""

    def populate(self, stock):
        """Populates the database with Stock objects."""
        currency = (
            stock.ticker
        )  # get name (ticker) for current Stock object to be updated
        base_currency = "USD"  # always compare against USD price
        url = "https://www.alphavantage.co/query?function=CURRENCY_EXCHANGE_RATE&from_currency={}&to_currency={}&apikey=WX0W0TEMMGW2CVT9".format(
            currency, base_currency
        )

        observation = requests.get(url=url).json()
        try:
            observation[
                "Realtime Currency Exchange Rate"
            ]  # check if we hit API rate limit
        except KeyError:  # means we hit API limit
            return None

        rate = observation["Realtime Currency Exchange Rate"][
            "5. Exchange Rate"
        ]  # get current exchange rate
        timestamp = datetime.datetime.now()
        stock.price = float(rate)  # turn string response into float
        stock.datetime = (
            timestamp  # update the timestamp for when the price was last recorded
        )
        stock.save()

        return self
