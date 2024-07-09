# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Install build dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    gcc \
    cmake \
    && rm -rf /var/lib/apt/lists/*

# Copy the requirements file into the container
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY app.py functions.py style.css ./

# Set environment variables
ENV REPO_ID="PrunaAI/Phi-3-mini-128k-instruct-GGUF-Imatrix-smashed"
ENV MODEL_FILE="Phi-3-mini-128k-instruct.Q4_K_S.gguf"
ENV API_KEY="c6dfc4d92a8f972d237ef696ec87b37a"

# Make port 7860 available to the world outside this container
EXPOSE 7860

# Run app.py when the container launches
CMD ["python", "app.py"]

