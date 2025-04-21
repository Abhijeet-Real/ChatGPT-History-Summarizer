import os
from multiprocessing import Pool, cpu_count
from QwenLoader import LLMEngine

def summarize_with_engine(chunk_path, summary_path, llm):
    with open(chunk_path, "r", encoding="utf-8") as f:
        text = f.read().strip()
    if not text:
        return

    prompt = f"""You are an expert assistant. Below is a raw conversation log.

Summarize only the content related to a speech-to-speech model pipeline.
Focus on ASR, TTS, STT, Whisper, NeMo, Bark, Gemma, VAD, queue systems, streaming.

### Conversation Log:
{text}

### Summary:"""

    summary = llm.generate(prompt)
    with open(summary_path, "w", encoding="utf-8") as out:
        out.write(summary)
    print(f"✅ Done: {summary_path}")

# ---------- CPU Worker ----------
llm = None
def init_worker_cpu(model_path):
    global llm
    if llm is None:
        llm = LLMEngine(model_path=model_path, ctx=32768, threads=6, gpu_layers=0)

def summarize_cpu(args):
    chunk_path, summary_path = args
    summarize_with_engine(chunk_path, summary_path, llm)

# ---------- Parallel Runner ----------
def parallel_summarize(base_folder, model_path):
    chunk_dir = os.path.join(base_folder, "chunk")
    summary_dir = os.path.join(base_folder, "summarize_chunk")
    os.makedirs(summary_dir, exist_ok=True)

    # Gather all chunk paths
    tasks = []
    for i in range(1, 1000):
        chunk_path = os.path.join(chunk_dir, f"chunk_{i}.ssf")
        if not os.path.exists(chunk_path):
            break
        summary_path = os.path.join(summary_dir, f"chunk_summary_{i}.ssf")
        tasks.append((chunk_path, summary_path))

    if not tasks:
        print("No chunks found.")
        return

    # Step 1: Run GPU summarizer on first chunk
    print("🧠 Summarizing chunk 1 on GPU...")
    gpu_llm = LLMEngine(model_path=model_path, ctx=32768, threads=6, gpu_layers=100)
    summarize_with_engine(*tasks[0], gpu_llm)

    # Step 2: Run CPU workers on remaining chunks
    cpu_tasks = tasks[1:]
    num_cpu_workers = min(4, len(cpu_tasks))  # Or use your estimate_parallel_workers()

    print(f"🔄 Summarizing remaining {len(cpu_tasks)} chunks with {num_cpu_workers} CPU workers...")
    with Pool(processes=num_cpu_workers, initializer=init_worker_cpu, initargs=(model_path,)) as pool:
        pool.map(summarize_cpu, cpu_tasks)

    print("🎯 All summaries complete!")

if __name__ == "__main__":
    folder = r"speech_to_speech"
    model = r"models/Qwen2-7B-Instruct/qwen2-7b-instruct-q4_k_m.gguf"
    parallel_summarize(folder, model)
