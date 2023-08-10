# Create your tests here.
import datetime
from unittest.mock import patch

from django.test import TestCase
from stocks.models import Stock
from stocks.tasks import populate_stock_price, sync_stocks


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
        self.assertEqual(
            Stock.objects.all().count(), 1
        )  # should be only 1 stock created in setup method
        sync_stocks()

        self.assertEqual(
            Stock.objects.all().count(), 4
        )  # should be 4 tasks after we add 3 more (as defined in tasks.py)

    @patch("stocks.tasks.Stock.objects.populate")  # patch the Stock.populate method
    def test_populate(self, stock_populate):
        """Test if the populate method is called when the periodic populate task beat runs."""
        populate_stock_price()
        stock_populate.assert_called()

    def test_populate_logic(self):
        """Test if the populate method actually updates the price of the stock."""
        sync_stocks()  # create stocks with 0 price
        stock = Stock.objects.get(ticker="BTC")
        self.assertTrue(stock.price == 0.0)  # confirm stock is created with price 0
        Stock.objects.populate(stock)  # populate the stock with price data from API
        self.assertFalse(stock.price == 0.0)  # should be different now
