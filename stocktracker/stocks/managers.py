import datetime

import requests
from celery.utils.log import get_task_logger
from decouple import config
from django.db import models

logger = get_task_logger(
    "populate_stock_price"
)  # to log to terminal when we hit API rate limit


class StockManager(models.Manager):
    """A manager for the Stock model."""

    def populate(self, stock):
        """Populates the database with Stock objects. This method is called by the populate_stock_price task periodically to keep stock prices updated in real time."""
        currency = (
            stock.ticker
        )  # get name (ticker) for current Stock object to be updated
        base_currency = "USD"  # always compare against USD price
        url = "https://www.alphavantage.co/query?function=CURRENCY_EXCHANGE_RATE&from_currency={}&to_currency={}&apikey={}".format(
            currency, base_currency, config("STOCK_API_KEY")
        )

        observation = requests.get(url=url).json()
        try:
            observation[
                "Realtime Currency Exchange Rate"
            ]  # check if we hit API rate limit
        except KeyError:  # means we hit API limit
            return logger.info(
                "ERROR: API rate limit reached. Task will be re-attempted later."
            )

        rate = observation["Realtime Currency Exchange Rate"][
            "5. Exchange Rate"
        ]  # get current exchange rate
        stock.price = float(rate)  # turn string response into float
        stock.datetime = (
            datetime.datetime.now()  # update the timestamp for when the price was last recorded
        )
        stock.save()

        return self
