import json

# Intent Rules
INTENT_RULES = {
    "rules": [
        {"id": 1, "pattern": "weather", "intent": "get_weather"},
        {"id": 2, "pattern": "temperature", "intent": "get_weather"},
        {"id": 3, "pattern": "forecast", "intent": "get_weather"},
        # Add more rules for other intents (e.g., "help", "goodbye") as needed
    ]
}

# Response Templates
RESPONSE_TEMPLATES = {
    "responses": [
        {
            "intent": "get_weather",
            "template": "The weather in {city} is: Temperature: {temp}°C, Description: {description}, Wind Speed: {wind_speed} m/s"
        },
        # Add more templates for other intents
    ]
}

# Function to load intent data
def load_intent_data(file_path):
    with open(file_path, "r") as f:
        data = json.load(f)
    return data
