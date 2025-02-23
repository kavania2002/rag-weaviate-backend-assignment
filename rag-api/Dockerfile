FROM python:3.12.4-slim

COPY . .

RUN pip install --upgrade pip && \
    pip install -r requirements.txt && \
    pip install "fastapi[standard]"


CMD ["fastapi", "run", "app/main.py"]
