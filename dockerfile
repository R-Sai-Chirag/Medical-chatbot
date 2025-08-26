# Use Python 3.12 slim image (latest patch, e.g., 3.12.11)
FROM python:3.12-slim-bookworm

# Set working directory
WORKDIR /app

COPY . /app

RUN pip install -r requirements.txt

CMD ["python3", "app.py"]