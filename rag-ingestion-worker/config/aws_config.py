import os
from dotenv import load_dotenv

load_dotenv()


class AWSConfig:
    """
    Configurations to connect with AWS Services
    """

    AWS_S3_BUCKET_NAME = os.getenv("AWS_S3_BUCKET_NAME")
    AWS_REGION = os.getenv("AWS_REGION", "ap-south-1")
    AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")


aws_config = AWSConfig()
