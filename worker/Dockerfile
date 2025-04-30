FROM python:3.13-slim

WORKDIR /bot

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app/ /bot/app

CMD ["celery", "-A", "app.celery_app.celery_app", "worker", "--loglevel=info"]
