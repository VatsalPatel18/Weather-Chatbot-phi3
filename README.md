# Weather Chatbot

An LLM Chatbot integrated with Open Weather API for Real-Time Weather Information.

## Features

- Get current weather information for any city.
- Get a 2-day weather forecast for any city.
- Utilizes `LangChain` for agent-based interactions.
- Runs on CPU using `llama-cpp-python`.
- Supports a context length of 128k tokens with the `phi-3-mini-128k-instruct-gguf` model.

## Installation

You can install the package using pip:

```bash
pip install weather-chatbot-phi3
```
## Useage 

```bash
from weather_chatbot import WeatherChatbot

chatbot = WeatherChatbot()
response = chatbot.get_weather("New York")
print(response)
```

## Under the Hood

This project leverages the power of `LangChain` for orchestrating the LLM interactions. Here's a breakdown of the key components:

### LangChain Agents and Tools

- **Agents**: LangChain's agent framework is used to create an intelligent assistant capable of performing specific tasks based on natural language inputs.
- **Tools**: Two main tools are integrated into the agent:
  - `WeatherLookup`: Fetches current weather data.
  - `ForecastLookup`: Retrieves weather forecast for the next two days.

### LLM with `llama-cpp-python`

The language model used is the `phi-3-mini-128k-instruct-gguf`, which supports a context length of 128k tokens. This model is run on the CPU using `llama-cpp-python`, ensuring that it can operate efficiently without the need for GPU resources.

## License

This project is licensed under the CC BY-NC-SA 4.0 License.
