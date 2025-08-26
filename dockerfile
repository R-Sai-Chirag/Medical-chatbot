# Use Python 3.12 slim image (latest patch, e.g., 3.12.11)
FROM python:3.12-slim-bookworm

# Set working directory
WORKDIR /app

# Copy requirements file
COPY requirements.txt .

# Install dependencies
RUN pip install --upgrade pip \
    && pip install -r requirements.txt 

# Copy application code
COPY . .

# Command to run the Flask app
CMD ["python3", "app.py"]