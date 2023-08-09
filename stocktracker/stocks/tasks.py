from celery import shared_task
from stocks.models import Stock


@shared_task
def add(x, y):
    return x + y


@shared_task
def get_stock_data():
    return "stock data"


@shared_task(
    autoretry_for=("PyOWMError",),
    retry_kwargs={"max_retries": 7, "countdown": 60},
)
def populate_stock_price():
    """A celery task to continously populate the database every hour the for
    all currently active stocks."""

    all_stocks = Stock.objects.all()
    for stock in all_stocks:
        Stock.objects.populate(stock)
