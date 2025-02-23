from celery import Celery
from celery.signals import worker_process_init, worker_process_shutdown
from config.redis_config import redis_config
from services.cache import RedisClient

celery_app = Celery(
    "rag_ingestion_worker",
    broker=redis_config.REDIS_URL,
    backend=redis_config.REDIS_URL,
    include=["worker.ingestion_worker", "worker.retrieval_worker"],
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    broker_connection_retry_on_startup=True,
)


@worker_process_init.connect
def init_worker(**_):
    """
    Initialize the worker"""
    print("Initializing worker...")
    RedisClient.connect()


@worker_process_shutdown.connect
def shutdown_worker(**_):
    """
    Shutdown the worker"""
    print("Shutting down worker...")
    RedisClient.close()


if __name__ == "__main__":
    print("Starting worker...")
    celery_app.start()
