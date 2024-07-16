# Use the official Python image as a base image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    GRADIO_SERVER_NAME="0.0.0.0" \
    REPO_ID="microsoft/Phi-3-mini-4k-instruct-gguf" \
    MODEL_FILE="Phi-3-mini-4k-instruct-q4.gguf"

# Create a working directory
WORKDIR /app

# Install dependencies for building C++ extensions and SSL
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential \
    cmake \
    openssl \
    wget \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy the requirements file
COPY requirements.txt /app/

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy SSL certificates
COPY certificates /app/certificates

# Copy the rest of the application code
COPY . /app/

# Create the cache directory with appropriate permissions
RUN mkdir -p /app/hf_cache && chmod -R 777 /app/hf_cache

# Manually download the required frpc file for Gradio share link
RUN wget -O /usr/local/lib/python3.11/site-packages/gradio/frpc_linux_amd64_v0.2 https://cdn-media.huggingface.co/frpc-gradio-0.2/frpc_linux_amd64
RUN chmod +x /usr/local/lib/python3.11/site-packages/gradio/frpc_linux_amd64_v0.2

# Ensure the model is downloaded
RUN python download_model.py

# Expose the port that Gradio will run on
EXPOSE 7860

# Set the user to root
USER root

# Run the application
CMD ["python", "app.py"]

