FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install OS dependencies needed for MongoDB TLS and DNS resolution
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    gnupg \
    libssl-dev \
    ca-certificates \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Uninstall pymongo to prevent conflicts with Motor
# RUN pip uninstall -y pymongo || true

# Copy app files
COPY . .

# Start the app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
