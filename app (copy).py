import gradio as gr
from llama_cpp import Llama
import requests

# Initialize the Llama model
llm = Llama(
    model_path="./phi3-gguf/Phi-3-mini-4k-instruct-q4.gguf",
    n_ctx=4096,
    n_threads=8,
    n_gpu_layers=0,
)

# OpenWeatherMap API settings
api_key = 'YOUR_OPENWEATHERMAP_API_KEY'

def get_weather(city):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        weather_description = data['weather'][0]['description']
        temp = data['main']['temp']
        wind_speed = data['wind']['speed']
        return f"Weather: {weather_description}, Temperature: {temp}°C, Wind Speed: {wind_speed} m/s"
    else:
        return "Could not fetch weather data. Please try again."

def respond(message, history):
    try:
        # Check if the message contains a weather query
        if 'weather' in message.lower():
            city = message.split()[-1]  # Assuming the city is the last word in the message
            weather_info = get_weather(city)
            return weather_info, history

        # Append the new message to the history
        history.append({"role": "user", "content": message})

        # Create the prompt based on the history
        prompt = "\n".join([f"{m['role']}: {m['content']}"] for m in history) + "\nassistant:"

        # Generate response
        output = llm(prompt, max_tokens=256, temperature=1.0, top_p=0.9, echo=False)
        response = output['choices'][0]['text'].strip()

        # Update history with the assistant's response
        history.append({"role": "assistant", "content": response})

        return response, history
    except Exception as e:
        return f"An error occurred: {e}", history

# Define the Gradio interface
demo = gr.Interface(
    fn=respond,
    inputs=[
        gr.Textbox(label="Ask a weather question or chat with the assistant", lines=2),
        gr.State([]),  # history
    ],
    outputs=[
        gr.Textbox(label="Response", lines=2),
        gr.State([]),  # updated history
    ],
    title="Weather Chatbot",
    description="Get real-time weather forecasts or chat with our assistant. Type your queries in natural language.",
    theme="huggingface",  # Use a light, friendly theme
    live=False
)

# Add a button for connecting to the Weather API (for demonstration)
def connect_weather_api():
    # This function can be expanded to handle actual connection logic
    return "Connected to OpenWeatherMap API"

demo.launch()

