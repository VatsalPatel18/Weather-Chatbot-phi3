# Use the official Python image as a base image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# Create a working directory
WORKDIR /app

# Install dependencies for building C++ extensions
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential \
    cmake \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy the requirements file
COPY requirements.txt /app/

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . /app/

# Ensure the model is downloaded
RUN python download_model.py

# Expose the port that Gradio will run on
EXPOSE 7860

# Run the application
CMD ["python", "app.py"]

