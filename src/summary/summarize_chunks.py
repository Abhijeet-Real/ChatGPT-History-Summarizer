import os
from LLMEngine.OllamaLoader import LLMEngine
from utils.log_message import log_message

# ---------- Summary Function ----------
def summarize_with_engine(base_folder, chunk_path, summary_path, llm):
    with open(chunk_path, "r", encoding="utf-8") as f:
        text = f.read().strip()
    if not text:
        return

    prompt = f"""Create extremely comprehensive and detailed summary of follwing text {text}"""

    if len(prompt) > 125000:
        log_message(base_folder, f"⚠️ Prompt too long ({len(prompt)} chars): {os.path.basename(chunk_path)}")


    summary = llm.generate(prompt)
    with open(summary_path, "w", encoding="utf-8") as out:
        out.write(summary)
    log_message(base_folder, f"✅ Done: {os.path.basename(summary_path)}")


# ---------- Single-GPU Runner ----------
def summarize_all_chunks(base_folder, model_name):
    chunk_dir = os.path.join(base_folder, "chunk")
    summary_dir = os.path.join(base_folder, "summarize_chunk")
    os.makedirs(summary_dir, exist_ok=True)

    llm = LLMEngine(model_name=model_name)

    for i in range(1, 1000):
        chunk_path = os.path.join(chunk_dir, f"chunk_{i}.ssf")
        summary_path = os.path.join(summary_dir, f"chunk_summary_{i}.ssf")

        if not os.path.exists(chunk_path):
            break

        if os.path.exists(summary_path):
            log_message(base_folder, f"⏩ Skipping: {os.path.basename(chunk_path)}")
            continue

        summarize_with_engine(base_folder, chunk_path, summary_path, llm)

    log_message(base_folder, "🎯 All summaries completed.") 

# ---------- Entry ----------
if __name__ == "__main__":
    folder = r"SIP"
    model_name = "mistral"  # or any other Ollama model
    summarize_all_chunks(folder, model_name)
