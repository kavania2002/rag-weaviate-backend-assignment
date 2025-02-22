from celery import Celery
from config.redis_config import redis_config

celery_app = Celery(
    "rag_ingestion_worker",
    broker=redis_config.REDIS_URL,
    backend=redis_config.REDIS_URL,
    include=["worker.ingestion_worker"],
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    broker_connection_retry_on_startup=True,
)

if __name__ == "__main__":
    print("Starting worker...")
    celery_app.start()
