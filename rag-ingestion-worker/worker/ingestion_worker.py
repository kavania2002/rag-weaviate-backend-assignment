from typing import List
from weaviate.collections.classes.data import DataObject
from celery_worker import celery_app

from services.db import WeaviateServices
from services.s3 import AWSS3
from worker.chunking import chunk_text
from worker.embeddings import generate_embedding


@celery_app.task
def generate_embeddings_from_file(file_key: str, file_name: str, file_type: str):
    """
    Celery task to generate embeddings and store them in Weaviate.
    """
    try:
        WeaviateServices.connect()
        file_content = AWSS3.get_file_content(file_key)
        text_parts = chunk_text(file_content)

        file_embeddings: List[DataObject] = []
        for doc in text_parts:
            file_embedding = DataObject(
                properties={
                    "file_id": file_key,
                    "chunk_content": doc.page_content,
                    "file_name": file_name,
                    "file_type": file_type,
                },
                vector=generate_embedding(doc.page_content),
            )
            file_embeddings.append(file_embedding)
        WeaviateServices.batch_write_file_embeddings(file_embeddings)

    except Exception as e:
        print(
            f"Unexpected failure while fetching {file_key} file and generating embeddings: {str(e)}"
        )
        raise RuntimeError(
            f"Unexpected failure while fetching {file_key} file and generating embeddings: {str(e)}"
        ) from e
    finally:
        WeaviateServices.close()
