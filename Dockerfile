FROM python:3.11-slim

WORKDIR /app

# System deps for audio, I2C, and image processing
RUN apt-get update && apt-get install -y --no-install-recommends \
    pkg-config \
    libavformat-dev \
    libavcodec-dev \
    libavdevice-dev \
    libavutil-dev \
    libswscale-dev \
    libswresample-dev \
    libavfilter-dev \
    libportaudio2 \
    libasound2-dev \
    libsndfile1 \
    i2c-tools \
    libi2c-dev \
    espeak-ng \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Install Piper TTS binary (aarch64 for Pi, amd64 for dev) \
#ARG TARGETARCH
#RUN if [ "$TARGETARCH" = "arm64" ]; then \
#      PIPER_URL="https://github.com/rhasspy/piper/releases/download/2023.11.14-2/piper_linux_aarch64.tar.gz"; \
#    else \
#      PIPER_URL="https://github.com/rhasspy/piper/releases/download/2023.11.14-2/piper_linux_x86_64.tar.gz"; \
#    fi && \
#    wget -qO- "$PIPER_URL" | tar -xz -C /usr/local/bin/

# Python deps
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# APP Code
COPY . .

# Expose NiceGUI port
EXPOSE 8080

# Run
CMD ["python", "app.py"]
