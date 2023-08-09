from django.db import models
from stocks.managers import StockManager


# Create your models here.
class Stock(models.Model):
    """A model to represent a stock publicy traded on an exchange."""

    ticker = models.CharField(max_length=3)  # ticker symbol for a given stock
    price = models.FloatField()  # to represent current exchange price

    datetime = models.DateTimeField()  # timestamp for when value was last updated

    objects = StockManager()  # custom manager for Stock model

    def __str__(self):
        return self.ticker
