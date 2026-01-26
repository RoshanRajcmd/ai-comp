# Stage 1: Build Stage (Needed for compiling certain Python packages)
FROM python:3.11-slim as builder

# Install necessary build tools and audio libraries
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libsndfile1 \
    libsndfile-dev \
    libgfortran5 \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements file and install dependencies
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

# Stage 2: Final Runtime Stage
FROM python:3.11-slim

# Install runtime dependencies for audio/science
RUN apt-get update && apt-get install -y --no-install-recommends \
    libsndfile1 \
    libgfortran5 \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy installed packages from the builder stage
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin/ /usr/local/bin/

# Copy application code
COPY . /app

# The Flask application listens on port 5000
EXPOSE 5000

# Command is defined in docker-compose.yml