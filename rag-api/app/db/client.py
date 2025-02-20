import os
from dotenv import load_dotenv

import weaviate
from weaviate import WeaviateAsyncClient
from weaviate.classes.init import Auth

load_dotenv()


class WeaviateClient:
    """
    A class to manage the Weaviate client connection
    """

    _async_client: WeaviateAsyncClient = None

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
        else:
            print("Failed to connect to Weaviate!")

    @staticmethod
    def is_connected():
        """Check if the client is connected"""
        if WeaviateClient._async_client:
            return WeaviateClient._async_client.is_connected()
        return False

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