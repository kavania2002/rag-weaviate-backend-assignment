from celery import Celery
from typing import List
from config.redis_config import redis_config


class CeleryService:
    _celery_client = Celery(
        "rag_ingestion_client",
        broker=redis_config.REDIS_URL,
        backend=redis_config.REDIS_URL,
    )

    _celery_client.conf.update(
        task_serializer="json",
        accept_content=["json"],
        result_serializer="json",
        timezone="UTC",
    )

    @staticmethod
    def send_task(task_name: str, queue: str, args: List[str]):
        """
        Send task to celery
        """
        CeleryService._celery_client.send_task(task_name, queue=queue, args=args)
        print(f"Task sent: {task_name}")
