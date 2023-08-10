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
        """Setup method that creates a non-existing stock to test how many
        Stocks the database will have after initialization.
        """
        timestamp = datetime.datetime.now()
        Stock.objects.create(ticker="AAPL", price=0.0, datetime=timestamp)

    def test_initialize(self):
        """Test if the sync_stocks task actually creates Stocks."""
        # Initially, there should only be 1 task in the database
        self.assertEqual(Stock.objects.all().count(), 1)
        sync_stocks()
        # Should be 4 tasks after we add 3 more with sync_stocks() (as defined
        # in tasks.py)
        self.assertEqual(Stock.objects.all().count(), 4)

    @patch("stocks.tasks.Stock.objects.populate")
    def test_populate(self, stock_populate):
        """Test if the populate method is called when the periodic populate
        task beat runs.
        """
        populate_stock_price()
        stock_populate.assert_called()

    def test_populate_logic(self):
        """Test if the populate method logic actually updates the price of the
        stock.
        """
        sync_stocks()  # Create all stocks with 0 price
        stock = Stock.objects.get(ticker="BTC")
        self.assertTrue(stock.price == 0.0)
        Stock.objects.populate(stock)
        self.assertFalse(stock.price == 0.0)
