import os
from typing import List
import uuid
from dotenv import load_dotenv

import weaviate
from weaviate import WeaviateAsyncClient
from weaviate.classes.init import Auth
from weaviate.classes.config import Configure, Property, DataType

load_dotenv()


class WeaviateClient:
    """
    A class to manage the Weaviate client connection
    """

    _async_client: WeaviateAsyncClient = None

    @staticmethod
    async def setup_weaviate_schema():
        """
        Setup the Weaviate schema
        """

        if not WeaviateClient.is_connected():
            print("Weaviate client not connected")
            return

        if await WeaviateClient._async_client.collections.exists("FileEmbeddings"):
            print("Collection already exists")
            return

        await WeaviateClient._async_client.collections.create(
            name="FileEmbeddings",
            description="Collection to store file embeddings",
            vector_index_config=Configure.VectorIndex.hnsw(),
            vectorizer_config=Configure.Vectorizer.none(),
            properties=[
                Property(name="chunk_id", data_type=DataType.TEXT),
                Property(name="chunk_content", data_type=DataType.TEXT),
                Property(name="file_name", data_type=DataType.TEXT),
                Property(name="file_type", data_type=DataType.TEXT),
            ],
        )

    @staticmethod
    async def connect():
        """Initialize the async client if not already initialized"""

        if WeaviateClient._async_client:
            print("Client already connected")
            return

        print("Connecting to Weaviate...")
        weaviate_url = os.getenv("WEAVIATE_URL")
        weaviate_api_key = os.getenv("WEAVIATE_API_KEY")

        WeaviateClient._async_client = weaviate.use_async_with_weaviate_cloud(
            cluster_url=weaviate_url,
            auth_credentials=Auth.api_key(weaviate_api_key),
        )
        await WeaviateClient._async_client.connect()

        if WeaviateClient._async_client.is_connected():
            print("Connected to Weaviate!")
            await WeaviateClient.setup_weaviate_schema()
        else:
            print("Failed to connect to Weaviate!")

    @staticmethod
    def is_connected():
        """Check if the client is connected"""
        if WeaviateClient._async_client:
            return WeaviateClient._async_client.is_connected()
        return False

    @staticmethod
    async def add_file_embedding(
        chunk_content: str,
        file_name: str,
        file_type: str,
        file_embedding: List[float],
    ):
        """
        Add file embeddings to Weaviate
        """
        if not WeaviateClient.is_connected():
            print("Weaviate client not connected")
            return

        file_embeddings_collection = WeaviateClient._async_client.collections.get(
            "FileEmbeddings"
        )

        await file_embeddings_collection.data.insert(
            properties={
                "chunk_id": uuid.uuid4().hex,
                "chunk_content": chunk_content,
                "file_name": file_name,
                "file_type": file_type,
            },
            vector=file_embedding,
        )

    @staticmethod
    async def get_file_embeddings():
        """
        Get file embeddings from Weaviate
        """
        if not WeaviateClient.is_connected():
            print("Weaviate client not connected")
            return

        file_embeddings_collection = WeaviateClient._async_client.collections.get(
            "FileEmbeddings"
        )

        return await file_embeddings_collection.length()

    @staticmethod
    async def close():
        """Close the client connection"""
        if WeaviateClient._async_client:
            print("Closing Weaviate connection...")
            await WeaviateClient._async_client.close()
            WeaviateClient._async_client = None
            print("Weaviate connection closed!")
        else:
            print("Client already closed")
