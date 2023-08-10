import datetime

from celery import shared_task
from stocks.models import Stock


@shared_task()
def populate_stock_price():
    """A celery task to periodically update the database for
    all unique tickers that exist in the database."""

    all_stocks = Stock.objects.all()
    for stock in all_stocks:
        Stock.objects.populate(stock)


@shared_task()
def sync_stocks():
    """A celery task to initialize(and keep in sync) the database with all unique
    tickers to keep track of."""
    tickers = [
        "BTC",
        "MATIC",
        "ETH",
    ]  # normally this would be an API call to get the list of tickers dynamically loaded in production
    # but results in too many API calls so mock data used here(rate limit)

    all_stocks = Stock.objects.all()
    for ticker in tickers:
        if not all_stocks.filter(
            ticker=ticker
        ).exists():  # if ticker doesn't exist in database, create it
            Stock.objects.create(
                ticker=ticker, price=0.0, datetime=datetime.datetime.now()
            )
