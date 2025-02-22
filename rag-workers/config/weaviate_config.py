import os
from dotenv import load_dotenv

load_dotenv()


class WeaviateConfig:
    """
    Configurations to connect with Weaviate
    """

    WEAVIATE_URL = os.getenv("WEAVIATE_URL")
    WEAVIATE_API_KEY = os.getenv("WEAVIATE_API_KEY")


weaviate_config = WeaviateConfig()
