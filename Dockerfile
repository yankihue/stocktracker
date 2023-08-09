FROM python:3.11.4-slim-bullseye
ENV PYTHONUNBUFFERED=1
WORKDIR /app

RUN python -m pip install --upgrade pip==20.2.4

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . /app/

EXPOSE $PORT

CMD ["bash", "entrypoint.sh"]
