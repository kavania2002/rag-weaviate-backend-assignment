from enum import Enum


class QueryStatus(str, Enum):
    SEND_TO_WORKER = "SEND_TO_WORKER"
    QUERYING = "QUERYING"
    ERROR = "ERROR"
