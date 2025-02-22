import json
from langchain_huggingface import HuggingFaceEmbeddings

from celery_worker import celery_app
from models.query_status import QueryStatus
from services.db import WeaviateServices
from services.cache import RedisClient

embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")


@celery_app.task
def query_embeddings(query_id: str, file_id: str, query: str):
    # TODO: might be a long query
    try:
        WeaviateServices.connect()
        query_vector = embeddings.embed_query(query)
        response = WeaviateServices.query_file_embeddings(file_id, query_vector)
        RedisClient.set(f"query_result:{query_id}", json.dumps(response))
        WeaviateServices.store_query_result(
            query_id, file_id, query, json.dumps(response)
        )
    except Exception as e:
        print(f"Failed to query embeddings: {e}")
        RedisClient.set(f"query_result:{query_id}", QueryStatus.ERROR)
        WeaviateServices.store_query_result(query_id, file_id, query, QueryStatus.ERROR)
    finally:
        WeaviateServices.close()
