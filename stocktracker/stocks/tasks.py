from celery import shared_task
from stocks.models import Stock


@shared_task()
def populate_stock_price():
    """A celery task to periodically update the database for
    all unique tickers that exist in the database."""

    all_stocks = Stock.objects.all()
    for stock in all_stocks:
        Stock.objects.populate(stock)
