import datetime

import requests
from celery.utils.log import get_task_logger
from decouple import config
from django.db import models

logger = get_task_logger(
    "populate_stock_price"
)  # To log to terminal when we hit API rate limit


class StockManager(models.Manager):
    """A manager for the Stock model."""

    def populate(self, stock):
        """Populates the database with Stock objects. This method is called by
        the populate_stock_price task periodically to keep stock prices
        updated in real time.
        """
        currency = stock.ticker
        base_currency = "USD"

        url = "https://www.alphavantage.co/query?function=CURRENCY_EXCHANGE_RATE&from_currency={}&to_currency={}&apikey={}".format(
            currency, base_currency, config("STOCK_API_KEY")
        )

        observation = requests.get(url=url).json()
        try:  # Check if we hit API rate limit
            observation["Realtime Currency Exchange Rate"]
        except KeyError:  # Means we hit API limit
            return logger.info(
                "ERROR: API rate limit reached. Task will be re-attempted later."
            )
        # Get current exchange rate for given ticker and
        # update the timestamp for when the price was last recorded
        rate = observation["Realtime Currency Exchange Rate"]["5. Exchange Rate"]
        stock.price = float(rate)
        stock.datetime = datetime.datetime.now()
        stock.save()

        return self
