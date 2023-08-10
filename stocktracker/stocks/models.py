from django.db import models
from stocks.managers import StockManager


# Create your models here.
class Stock(models.Model):
    """A model to represent a stock publicy traded on an exchange. Ticker
    symbol, price, and datetime are required fields.
    """

    ticker = models.CharField(max_length=5)  # Ticker symbol for a given stock
    price = models.FloatField()

    datetime = models.DateTimeField()  # Timestamp
    objects = StockManager()  # Custom manager for Stock model

    def __str__(self):
        return self.ticker
