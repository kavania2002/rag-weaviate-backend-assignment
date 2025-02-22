from typing import List
import uuid

import weaviate
from weaviate.client import WeaviateClient
from weaviate.classes.init import Auth
from weaviate.collections.classes.data import DataObject

from config.weaviate_config import weaviate_config


class WeaviateServices:
    """
    A class to manage the Weaviate client connection
    """

    _client: WeaviateClient = None

    @staticmethod
    def connect():
        """Initialize the async client if not already initialized"""

        if WeaviateServices._client:
            print("Client already connected")
            return

        print("Connecting to Weaviate...")

        WeaviateServices._client = weaviate.connect_to_weaviate_cloud(
            cluster_url=weaviate_config.WEAVIATE_URL,
            auth_credentials=Auth.api_key(weaviate_config.WEAVIATE_API_KEY),
        )

        if WeaviateServices._client.is_connected():
            print("Connected to Weaviate!")
        else:
            print("Failed to connect to Weaviate!")

    @staticmethod
    def is_connected():
        """Check if the client is connected"""
        if WeaviateServices._client:
            return WeaviateServices._client.is_connected()
        return False

    @staticmethod
    def add_file_embedding(
        file_id: str,
        chunk_content: str,
        file_name: str,
        file_type: str,
        file_embedding: List[float],
    ):
        """
        Add file embeddings to Weaviate
        """
        if not WeaviateServices.is_connected():
            print("Weaviate client not connected")
            return

        file_embeddings_collection = WeaviateServices._client.collections.get(
            "FileEmbeddings"
        )

        file_embeddings_collection.data.insert(
            properties={
                "file_id": file_id,
                "chunk_id": uuid.uuid4().hex,
                "chunk_content": chunk_content,
                "file_name": file_name,
                "file_type": file_type,
            },
            vector=file_embedding,
        )

    @staticmethod
    def batch_write_file_embeddings(file_embeddings: List[DataObject]):
        """
        Add multiple file embeddings to Weaviate
        """
        if not WeaviateServices.is_connected():
            print("Weaviate client not connected")
            return

        file_embeddings_collection = WeaviateServices._client.collections.get(
            "FileEmbeddings"
        )

        with file_embeddings_collection.batch.dynamic() as batch:
            for file_embedding in file_embeddings:
                batch.add_object(
                    properties=file_embedding.properties, vector=file_embedding.vector
                )

                if batch.number_errors > 10:
                    print("Batch write failed, rolling back")
                    return

        failed_objects = file_embeddings_collection.batch.failed_objects
        if failed_objects:
            print(f"Failed to batch write {len(failed_objects)} objects")
        else:
            print("Batch write successful")

    @staticmethod
    def close():
        """Close the client connection"""
        if WeaviateServices._client:
            print("Closing Weaviate connection...")
            WeaviateServices._client.close()
            WeaviateServices._client = None
            print("Weaviate connection closed!")
        else:
            print("Client already closed")
