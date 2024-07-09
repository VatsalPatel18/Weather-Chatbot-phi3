import os
import gradio as gr
from langchain.agents import Tool
from langchain_community.llms import LlamaCpp  # Use langchain_community
from langchain.agents import initialize_agent
from functions import get_weather_info, get_forecast, restructure_forecast
from huggingface_hub import hf_hub_download  
import json
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize the LlamaCpp model
llm = LlamaCpp(
    model_path=hf_hub_download(
        repo_id=os.environ.get("REPO_ID", "PrunaAI/Phi-3-mini-128k-instruct-GGUF-Imatrix-smashed"),
        filename=os.environ.get("MODEL_FILE", "Phi-3-mini-128k-instruct.Q4_K_S.gguf"),
    ),
    n_ctx=4096*15,
    n_gpu_layers=-1
)

# Define tools
weather_tool = Tool(
    name="WeatherLookup",
    func=lambda city: get_weather_info(city),
    description="Useful to get the current weather (Today) information for a city. It includes information on temperature, pressure, humidity, wind, clouds, and rain."
)

forecast_tool = Tool(
    name="ForecastLookup",
    func=lambda city: get_forecast(city),
    description="Useful to get the weather forecast for the next three days for a city. It includes information on temperature, pressure, humidity, wind, clouds, and rain."
)

# Tools (Include both Weather and Forecast Tools)
tools = [weather_tool, forecast_tool]

# Initialize Agent
agent = initialize_agent(tools, llm, agent="zero-shot-react-description", verbose=True)

def respond(message, history):
    try:
        # Create the prompt based on the history
        prompt = "\n".join([f"{'User' if i % 2 == 0 else 'Assistant'}: {m[0]}" for i, m in enumerate(history)]) + "\nAssistant:"

        # Generate response using LangChain agent
        response = agent.run(message)
        
        # Update history with the assistant's response
        history.append((message, response))

        return response, history
    except Exception as e:
        return f"An error occurred: {e}", history

# Define the Gradio interface
with gr.Blocks(css="style.css") as demo:
    gr.Markdown(
        """
        # Weather Chatbot
        Get real-time weather forecasts or chat with our assistant. Type your queries in natural language.
        """
    )
    with gr.Row():
        with gr.Column():
            message = gr.Textbox(label="Ask a weather question or chat with the assistant", lines=2, placeholder="Type your question here...")
            response = gr.Textbox(label="Response", lines=2)
            state = gr.State([])
            btn = gr.Button("Submit")
            btn.click(respond, [message, state], [response, state])
    
    gr.Examples(
        examples=[
            ["What's the weather in New York?"],
            ["Tell me the weather forecast for Tokyo."],
            ["What's the temperature in London?"]
        ],
        inputs=message
    )

# Launch the Gradio interface
def main():
    demo.launch(share=True, debug=True)

if __name__ == "__main__":
    main()

