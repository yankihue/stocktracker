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
        sync_stocks()

        self.assertEqual(
            Stock.objects.all().count(), 4
        )  # should be 4 tasks after we add 3 more (as defined in tasks.py)

    @patch("stocks.tasks.Stock.objects.populate")  # patch the Stock.populate method
    def test_populate_is_called(self, stock_populate):
        """Test if the populate method is called when the periodic populate task beat runs."""
        populate_stock_price()
        stock_populate.assert_called()
