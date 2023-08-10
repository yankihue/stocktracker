# Stocktracker

This is a project based on Django REST Framework and Celery(using Redis as a broker) to keep track of stock prices. Live prices are queried from (www.alphavantage.co)[Alpha Vantage] periodically using celery beats and the corresponding stock tickers are updated in the database. As the API is rate limited, the number of stocks to keep track of and the frequency of updates has been intentionally lowered. 

## Development Environment
For linting `Flake8` has been utilized as well as `Black` for styling. Imports are sorted on file save using `isort`.

## Deployment
The docker-compose file in the root directory sets up the project in a development environment locally. Create a `.env` file corresponding with the example and fill out the missing variables. Then

```bash
docker-compose build
docker-compose up # or docker-compose up -d
```
should deploy the project on localhost:8010. Head to the `/stocks` directory to observe the stock prices and timestamps being updated. You can check the results of the celery tasks from the `/admin` directory.


This configuration can be used as a starting point to deploy the app to a provider as well.