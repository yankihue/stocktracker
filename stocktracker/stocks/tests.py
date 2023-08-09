# Create your tests here.
import datetime

from django.test import TestCase
from stocks.models import Stock
from stocks.tasks import initialize_stocks, populate_stock_price


class DefaultTest(TestCase):
    def setUp(self):
        pass

    def test_X(self):
        self.assertEqual(3, 3)


class StockTest(TestCase):
    def setUp(self):
        timestamp = datetime.datetime.now()
        Stock.objects.create(
            ticker="AAPL", price=0.0, datetime=timestamp
        )  # add a non-existing stock to test how many the database will have after initialization

    def test_initialize(self):
        initialize_stocks.apply()

        self.assertEqual(
            Stock.objects.all().count(), 4
        )  # should be 4 tasks after we add 3 more (as defined in tasks.py)

    def test_populate_task(self):
        timestamp = datetime.datetime.now()
        Stock.objects.create(ticker="XMR", price=0.0, datetime=timestamp)
        populate_stock_price.apply()  # call task synchronously (no queueing) and locally (in the same process)
        self.assertTrue(
            Stock.objects.get(ticker="XMR").price != 0.0
        )  # check if price was updated. should be different than 0
        self.assertTrue(
            Stock.objects.get(ticker="XMR").datetime != timestamp
        )  # check if timestamp was updated. should be different from the initial time
