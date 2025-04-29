FROM python:3.13-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app/ app/
COPY celery_app.ry .

CMD ["celery", "-A", "celery_app.celery", "worker", "--loglevel=info"]
