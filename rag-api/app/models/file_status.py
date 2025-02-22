from enum import Enum


class FileStatus(str, Enum):
    UPLOADING_TO_S3 = "UPLOADING_TO_S3"
    UPLOADED_TO_S3 = "UPLOADED_TO_S3"
    SENT_TO_WORKER = "SENT_TO_WORKER"
    GENERATING_EMBEDDINGS = "GENERATING_EMBEDDINGS"
    EMBEDDINGS_GENERATED = "EMBEDDINGS_GENERATED"
    ERROR_OCCURRED = "ERROR_OCCURRED"
    FAILED = "FAILED"
