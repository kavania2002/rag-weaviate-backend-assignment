import boto3
from botocore.exceptions import BotoCoreError, NoCredentialsError
from config.aws_config import aws_config


class AWSS3:
    _s3_client = boto3.client(
        "s3",
        aws_access_key_id=aws_config.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=aws_config.AWS_SECRET_ACCESS_KEY,
        region_name=aws_config.AWS_REGION,
    )
    _bucket_name = aws_config.AWS_S3_BUCKET_NAME

    @staticmethod
    def get_file_content(file_key: str) -> bytes:
        """
        Get file from S3 bucket
        """

        try:
            response = AWSS3._s3_client.get_object(
                Bucket=AWSS3._bucket_name, Key=file_key
            )
            return response["Body"].read()
        except NoCredentialsError as e:
            raise RuntimeError("AWS credentials are missing or incorrect") from e
        except BotoCoreError as e:
            raise RuntimeError(
                f"Failed to get {file_key} due to AWS error: {str(e)}"
            ) from e
        except Exception as e:
            raise RuntimeError(f"Unexpected error getting {file_key}: {str(e)}") from e
