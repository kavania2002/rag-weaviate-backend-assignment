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
    def upload_file(key: str, file_content: bytes):
        try:
            AWSS3._s3_client.put_object(
                Bucket=AWSS3._bucket_name,
                Key=key,
                Body=file_content,
            )
            print(f"Upload successful: {key}")
        except NoCredentialsError as e:
            raise RuntimeError("AWS credentials are missing or incorrect") from e
        except BotoCoreError as e:
            raise RuntimeError(
                f"Failed to upload {key} due to AWS error: {str(e)}"
            ) from e
        except Exception as e:
            raise RuntimeError(f"Unexpected error uploading {key}: {str(e)}") from e
