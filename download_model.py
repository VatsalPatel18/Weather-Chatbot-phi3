import os
from huggingface_hub import hf_hub_download

def download_model():
    model_path = "./model/phi-3-gguf/Phi-3-mini-4k-instruct-q4.gguf"
    if not os.path.exists(model_path):
        hf_hub_download(
            repo_id="microsoft/Phi-3-mini-4k-instruct-gguf",
            filename="Phi-3-mini-4k-instruct-q4.gguf",
            local_dir="model/phi-3-gguf"
        )

if __name__ == "__main__":
    download_model()

