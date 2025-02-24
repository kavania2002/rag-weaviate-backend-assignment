FROM python:3.12.4-slim

COPY . .

RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir "fastapi[standard]"


CMD ["fastapi", "run", "app/main.py"]
