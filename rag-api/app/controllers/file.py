from services.embeddings import generate_embeddings
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
            AWSS3.upload_file(f"{file_id}.{file_type}", file_content)
            # await generate_embeddings(file_id, file_content, file_name, file_type)
            # print("Embeddings generated")
        except RuntimeError as e:
            raise RuntimeError(f"Failed to upload {file_id} to S3") from e

        except Exception as e:
            raise RuntimeError(f"Unexpected failure while uploading {file_id}") from e
