from typing import List
import uuid

import weaviate
from weaviate.client import WeaviateAsyncClient
from weaviate.classes.init import Auth
from weaviate.classes.config import Configure, Property, DataType
from weaviate.classes.query import Filter, MetadataQuery

from config.weaviate_config import weaviate_config


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
            print("FileEmbeddings collection already exists")
        else:
            await WeaviateClient._async_client.collections.create(
                name="FileEmbeddings",
                description="Collection to store file embeddings",
                vector_index_config=Configure.VectorIndex.hnsw(),
                vectorizer_config=Configure.Vectorizer.none(),
                properties=[
                    Property(name="file_id", data_type=DataType.TEXT),
                    Property(name="chunk_id", data_type=DataType.TEXT),
                    Property(name="chunk_content", data_type=DataType.TEXT),
                    Property(name="file_name", data_type=DataType.TEXT),
                    Property(name="file_type", data_type=DataType.TEXT),
                ],
            )

        if await WeaviateClient._async_client.collections.exists("FileStatus"):
            print("FileStatus collection already exists")
        else:
            await WeaviateClient._async_client.collections.create(
                name="FileStatus",
                description="Class to store file status",
                vectorizer_config=Configure.Vectorizer.none(),
                properties=[
                    Property(name="file_id", data_type=DataType.TEXT),
                    Property(name="status", data_type=DataType.TEXT),
                    Property(name="message", data_type=DataType.TEXT),
                ],
            )

        if await WeaviateClient._async_client.collections.exists("QueryResults"):
            print("QueryResults collection already exists")
        else:
            await WeaviateClient._async_client.collections.create(
                name="QueryResults",
                description="Collection to store query results",
                vector_index_config=Configure.VectorIndex.hnsw(),
                vectorizer_config=Configure.Vectorizer.none(),
                properties=[
                    Property(name="file_id", data_type=DataType.TEXT),
                    Property(name="query_id", data_type=DataType.TEXT),
                    Property(name="query_content", data_type=DataType.TEXT),
                    Property(name="result", data_type=DataType.TEXT),
                ],
            )

    @staticmethod
    async def connect():
        """Initialize the async client if not already initialized"""

        if WeaviateClient._async_client:
            print("Client already connected")
            return

        print("Connecting to Weaviate...")

        WeaviateClient._async_client = weaviate.use_async_with_weaviate_cloud(
            cluster_url=weaviate_config.WEAVIATE_URL,
            auth_credentials=Auth.api_key(weaviate_config.WEAVIATE_API_KEY),
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
    async def get_file_status(file_id: str):
        """
        Get the status of the file
        """
        if not WeaviateClient.is_connected():
            print("Weaviate client not connected")
            return

        file_status_collection = WeaviateClient._async_client.collections.get(
            "FileStatus"
        )

        response = await file_status_collection.query.fetch_objects(
            filters=Filter.by_property("file_id").equal(file_id)
        )

        if response.objects:
            return response.objects[0].properties.get("status")
        return None

    @staticmethod
    async def get_query_status(query_id: str):
        """
        Get the status of the query
        """
        if not WeaviateClient.is_connected():
            print("Weaviate client not connected")
            return

        query_results_collection = WeaviateClient._async_client.collections.get(
            "QueryResults"
        )

        response = await query_results_collection.query.fetch_objects(
            filters=Filter.by_property("query_id").equal(query_id)
        )

        if response.objects:
            return response.objects[0].properties.get("result")
        return None

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
