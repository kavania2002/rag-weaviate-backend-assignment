from models.query_status import QueryStatus
from services.db import WeaviateClient
from services.cache import RedisClient
from services.celery import CeleryService


class QueryController:
    """
    Query Controller
    """

    @staticmethod
    def query_file(query_id: str, file_id: str, query: str):
        """
        Query file
        """

        try:
            RedisClient.set(f"query_result:{query_id}", QueryStatus.QUERYING)
            CeleryService.send_task(
                "worker.retrieval_worker.query_embeddings",
                queue="retrieval_worker",
                args=[query_id, file_id, query],
            )
        except RuntimeError as e:
            raise RuntimeError(
                f"Failed to query {file_id} with query_id {query_id}"
            ) from e
        except Exception as e:
            raise RuntimeError(
                f"Unexpected failure while querying {file_id} with query_id {query_id}"
            ) from e

    @staticmethod
    async def get_query_status(query_id: str):
        """
        Get query status
        """
        redis_key = f"query_result:{query_id}"
        if RedisClient.exists(redis_key):
            return RedisClient.get(redis_key)

        response = await WeaviateClient.get_query_status(redis_key)
        return response
