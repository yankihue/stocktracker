from django.db import models
from stocks.managers import StockManager


# Create your models here.
class Stock(models.Model):
    ticker = models.CharField(max_length=10)
    price = models.FloatField()

    datetime = models.DateTimeField()

    objects = StockManager()

    def __str__(self):
        return self.ticker
