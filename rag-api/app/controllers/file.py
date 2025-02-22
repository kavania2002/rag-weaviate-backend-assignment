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
        # add task to celery queue

        try:
            file_key = f"{file_id}.{file_type}"
            RedisClient.set(file_key, FileStatus.UPLOADING_TO_S3)
            AWSS3.upload_file(file_key, file_content)
            RedisClient.set(file_key, FileStatus.SENT_TO_WORKER)
            CeleryService.send_task(
                "worker.ingestion_worker.generate_embeddings_from_file",
                [file_key, file_name, file_type],
            )
        except RuntimeError as e:
            raise RuntimeError(f"Failed to upload {file_id} to S3") from e

        except Exception as e:
            raise RuntimeError(f"Unexpected failure while uploading {file_id}") from e

    @staticmethod
    async def get_file_status(file_id: str):
        """
        Get file status
        """
        if RedisClient.exists(file_id):
            return RedisClient.get(file_id)

        response = await WeaviateClient.get_file_status(file_id)
        return response
