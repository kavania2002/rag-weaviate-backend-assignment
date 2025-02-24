# FastAPI Server

## Overview

This repository contains the FastAPI server for handling file uploads, query processing, and status tracking. It interacts with external services such as Redis, S3, Weaviate, and Celery workers for efficient processing.

## Features

- File upload and status tracking
- Query submission and status tracking
- Integration with Redis for caching
- Interaction with S3 for file storage
- Weaviate for result and status retrieval (act as persistant storage)
- Celery workers for background processing

## Folder Structure

```
app/
|-- config/           # Configuration files for external services
|   |-- aws_config.py
|   |-- redis_config.py
|   |-- weaviate_config.py
|
|-- controllers/      # Business logic for handling files and queries
|   |-- file.py
|   |-- query.py
|
|-- models/          # Data models for file and query status
|   |-- file_status.py
|   |-- query_status.py
|
|-- routes/          # API routes definitions
|   |-- __init__.py
|   |-- file.py
|   |-- health.py
|   |-- query.py
|
|-- services/        # Services for handling caching, database, and storage
|   |-- cache.py
|   |-- celery.py
|   |-- db.py
|   |-- s3.py
|
|-- utils/           # Utility functions and constants
|   |-- constants.py
|   |-- response.py
|
|-- main.py          # Entry point of FastAPI server
```

## Setup & Installation

### Prerequisites

- Python 3.12+
- Redis (DB Cache and Broker)
- AWS S3
- Weaviate
- Celery

### Installation Steps

1. Create a virtual environment and activate it:
   ```sh
   python -m venv .venv
   source .venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```
2. Install dependencies:
   ```sh
   pip install -r requirements.txt
   pip install "fastapi[standard]"
   ```
3. Set up environment variables:
   - Copy `.env.example` to `.env`
   - Fill in required values such as database URL, Redis config, and AWS credentials
4. Run the FastAPI server:
   ```sh
   fastapi dev app/main.py
   ```

## API Endpoints

| Method | Endpoint                       | Description                  |
| ------ | ------------------------------ | ---------------------------- |
| POST   | `/api/file/upload`             | Upload a file                |
| GET    | `/api/file/status/{file_id}`   | Get file processing status   |
| POST   | `/api/query/{file_id}`         | Submit a query using file_id |
| GET    | `/api/query/status/{query_id}` | Get query processing status  |
| GET    | `/health`                      | Check API health             |
| GET    | `/`                            | Ping Endpoint                |

## Deployment

To deploy the FastAPI server using Docker:

```sh
docker build -t rag-ai-backend .
docker run -p 8000:8000 --env-file .env rag-ai-backend
```

### Current Deployment

- Deployed in AWS ECS as an ECS Task
- Public Image: [kavania2002/rag-ai-backend](https://hub.docker.com/r/kavania2002/rag-ai-backend)

## TODOs

- Add Rate Limiter
