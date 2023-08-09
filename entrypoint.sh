#!/usr/bin/env bash
set -e

python3 manage.py makemigrations
python3 manage.py migrate
gunicorn stocktracker.wsgi:application -b 0.0.0.0:8080

# exec "$@"
