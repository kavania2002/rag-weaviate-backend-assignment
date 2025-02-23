FROM python:3.12-slim

COPY requirements.txt requirements.txt

RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    && rm -rf /var/lib/apt/lists/* && \
    pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["sh", "-c", "celery -A celery_worker.celery_app worker --loglevel=info --queues ingestion_worker & celery -A celery_worker.celery_app worker --loglevel=info --queues retrieval_worker"]
