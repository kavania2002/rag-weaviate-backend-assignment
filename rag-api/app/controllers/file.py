from models.file_status import FileStatus
from services.cache import RedisClient
from services.celery import CeleryService
from services.db import WeaviateClient
from services.s3 import AWSS3


class FileController:
    """
    File Controller
    """

    @staticmethod
    def upload_file(file_id: str, file_content: bytes, file_name: str, file_type: str):
        """
        Upload file to S3
        """

        try:
            file_key = f"{file_id}.{file_type}"
            RedisClient.set(f"file_status:{file_key}", FileStatus.UPLOADING_TO_S3)
            AWSS3.upload_file(file_key, file_content)
            RedisClient.set(f"file_status:{file_key}", FileStatus.UPLOADED_TO_S3)
            CeleryService.send_task(
                "worker.ingestion_worker.generate_embeddings_from_file",
                queue="ingestion_worker",
                args=[file_key, file_name, file_type],
            )
            RedisClient.set(f"file_status:{file_key}", FileStatus.SENT_TO_WORKER)
        except RuntimeError as e:
            raise RuntimeError(f"Failed to upload {file_id} to S3") from e

        except Exception as e:
            raise RuntimeError(f"Unexpected failure while uploading {file_id}") from e

    @staticmethod
    async def get_file_status(file_id: str):
        """
        Get file status
        """
        redis_key = f"file_status:{file_id}"
        if RedisClient.exists(redis_key):
            return RedisClient.get(redis_key)

        response = await WeaviateClient.get_file_status(redis_key)
        return response
