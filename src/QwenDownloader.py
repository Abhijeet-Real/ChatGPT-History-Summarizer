from huggingface_hub import hf_hub_download
import os

def download_qwen2_7b_q4km(local_dir="models/Qwen2-7B-Instruct"):
    model_file = "qwen2-7b-instruct-q4_k_m.gguf"
    repo_id = "Qwen/Qwen2-7B-Instruct-GGUF"
    
    os.makedirs(local_dir, exist_ok=True)

    print("🔽 Downloading Qwen2-7B-Instruct Q4_K_M...")
    model_path = hf_hub_download(
        repo_id=repo_id,
        filename=model_file,
        local_dir=local_dir
    )

    print(f"✅ Model downloaded to: {model_path}")
    return model_path

if __name__ == "__main__":
    download_qwen2_7b_q4km()
