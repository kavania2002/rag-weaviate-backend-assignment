# rag-worker

- `celery -A celery_worker.celery_app worker --loglevel=info --concurrency=4 --queues ingestion_worker`
- `celery -A celery_worker.celery_app worker --loglevel=info --concurrency=4 --queues retrieval_worker`
