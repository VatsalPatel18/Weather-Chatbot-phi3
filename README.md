Weather Chatbot - Docker Version
================================

An LLM Chatbot integrated with Open Weather API for Real-Time Weather Information.

Features
--------
- Get current weather information for any city.
- Get a 2-day weather forecast for any city.
- Utilizes LangChain for agent-based interactions.
- Runs on CPU using llama-cpp-python.
- Supports a context length of 128k tokens with the phi-3-mini-128k-instruct-gguf model.

Installation and Usage
----------------------

To use this application with Docker, follow these steps:

1. Clone the repository:
git clone https://github.com/username/Weather-Chatbot-phi3.git
cd Weather-Chatbot-phi3


2. Switch to the Docker branch:
git checkout docker

3. Build the Docker image:
docker build -t weather-chatbot .


4. Run the Docker container:
docker run -p 7860:7860 weather-chatbot


This will start the Gradio interface on port 7860. Open your web browser and go to `http://localhost:7860` to interact with the chatbot.

Project Structure
-----------------
- `app.py`: Main application file that sets up and runs the Gradio interface.
- `Dockerfile`: Defines the Docker image for the application.
- `download_model.py`: Script to download the necessary model files.
- `functions.py`: Contains the functions for weather information and forecast retrieval.
- `requirements.txt`: Lists the Python dependencies for the project.
- `style.css`: Contains custom styles for the Gradio interface.

License
-------
This project is licensed under the CC BY-NC-SA 4.0 License.

Author
------
Vatsal Patel


