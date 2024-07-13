import os
from huggingface_hub import hf_hub_download

def download_model():
    model_path = "./model/phi-3-gguf/Phi-3-mini-128k-instruct.Q4_K_S.gguf"
    if not os.path.exists(model_path):
        hf_hub_download(
            repo_id="PrunaAI/Phi-3-mini-128k-instruct-GGUF-Imatrix-smashed",
            filename="Phi-3-mini-128k-instruct.Q4_K_S.gguf",
            local_dir="model/phi-3-gguf"
        )

if __name__ == "__main__":
    download_model()

