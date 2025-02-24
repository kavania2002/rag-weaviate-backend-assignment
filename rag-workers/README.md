# Workers README

## Overview

This module contains two Celery workers responsible for file ingestion and query retrieval in the Retrieval-Augmented Generation (RAG) pipeline. These workers process uploaded documents, generate vector embeddings, store them in Weaviate, and retrieve relevant results based on user queries.

## Worker Types

### 1. **Ingestion Worker**

- Extracts text from uploaded files.
- Processes the text according to file type.
  - Used OCR based method for PDF (used `PyMuPDF)
  - Used `python-docx` to read docx
- Used langchain's `RecursiveCharacterTextSplitter` and `RecursiveJsonSplitter`
- Converts text into vector embeddings using sentence-transformer's `paraphrase-MiniLM-L3-v2` model.
- Stores embeddings in Weaviate.
- Updates Redis with processing status.

### 2. **Retrieval Worker**

- Takes a user query and finds relevant embeddings in Weaviate.
- Retrieves top-matching document chunks.
- Constructs a response and caches it in Redis.
- Updates query processing status.

## Folder Structure

```
config/
  ├── aws_config.py         # AWS configuration settings
  ├── redis_config.py       # Redis configuration settings
  ├── weaviate_config.py    # Weaviate configuration settings

models/
  ├── file_status.py        # Model for file status tracking
  ├── query_status.py       # Model for query status tracking

services/
  ├── cache.py              # Caching service
  ├── db.py                 # Database interactions
  ├── s3.py                 # S3 interactions

worker/
  ├── chunking.py           # Handles document chunking
  ├── embeddings.py         # Embedding generation
  ├── ingestion_worker.py   # Ingestion worker process
  ├── retrieval_worker.py   # Retrieval worker process

celery_worker.py            # Celery worker initialization
```

## Setup Instructions

### Prerequisites

- Redis (as Celery broker and cache)
- Weaviate (for vector storage)
- AWS S3 (for file storage)
- Celery
- Python 3.12+

### Installation

```bash
pip install -r requirements.txt
sudo apt-get install -y tesseract-ocr
```

### Running the Workers

Start the Celery workers with the following command:

```bash
celery -A celery_worker.celery_app worker --loglevel=info --queues ingestion_worker & \
celery -A celery_worker.celery_app worker --loglevel=info --queues retrieval_worker
```

## Current Deployment

- Currently deployed on EC2
- Used `ssh` and copy files into the VM
- Used `tmux` to keep the workers on

## TODOs

- Explore more better approach for chunking and extraction of text from each type
- Try semantic chunking as well as retrieval
- Learn more about deployment of these heavy tasks
