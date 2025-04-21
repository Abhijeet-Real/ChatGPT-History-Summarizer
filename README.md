
# 🧠 ChatGPT History Summarizer 🔍

This project enables fully local, customizable summarization of your exported ChatGPT conversation history — with the ability to extract, clean, chunk, and summarize only the most relevant content (e.g., Speech-to-Speech, STT, TTS, ASR pipelines).

---

## 🚀 Features

✅ **Extracts** only messages relevant to your topic (e.g., S2S, Whisper, Bark, NeMo, etc.)  
✅ **Cleans** and removes redundant code, markdown, or irrelevant meta-text  
✅ **Chunks** cleaned content into manageable parts  
✅ **Summarizes** using a 7B model (Qwen2-7B-GGUF) locally on your CPU/GPU  
✅ **Hybrid Inference**: GPU handles 1 summary, rest run in parallel via CPU  
✅ **Fully Modular**: Easy to plug in your own model or keywords

---

## 🧩 Folder Structure

```
History/
├── keywords.ssf               # Your topic-specific keywords (e.g. tts, vad, whisper...)
├── extracted history.ssf      # Auto-generated: filtered relevant messages
├── cleaned history.ssf        # Auto-generated: cleaned for LLM
├── chunk/                     # Auto-generated: chunked files for summarization
└── summarize_chunk/           # Auto-generated: summary of each chunk
```

```
src/
├── extract_history.py         # Extracts relevant messages from ChatGPT JSON
├── clean_history.py           # Cleans up code blocks and noise
├── create_chunk.py            # Chunks cleaned content (with overlap)
├── QwenSummarizer.py          # Loads GGUF model using llama-cpp-python
├── QwenDownloader.py          # Downloads model using huggingface_hub
├── QwenLoader.py              # GPU/CPU hybrid model loading logic
├── HuggingFaceLogin.py        # Handles token-based login
├── history_pipeline.py        # One-click pipeline runner
└── requirements.txt
```

---

## 🛠 How to Run

> ⚠️ Requires 6 GB+ VRAM (GPU) and ~24 GB RAM (CPU parallel inference)

### 1. 🧹 Run the Full Pipeline
```bash
python src/history_pipeline.py
```

### 2. 📦 Summarize (Hybrid CPU + GPU)
```bash
python src/run_summarizer.py
```

---

## 📂 Input Format

Use ChatGPT's export (`conversations.json`)  
Place it in:  
```plaintext
OpenAI April 2025/conversations.json
```

---

## 🔥 Models

We use `Qwen2-7B-Instruct-GGUF` in quantized `Q4_K_M` format for blazing-fast local inference.

📦 Can be switched to any GGUF LLM using `QwenSummarizer.py`

---

## 🧠 Examples of Use

- Speech-to-Speech research logs 🗣️→🗣️  
- Extracting just **NLP project** discussions from long chats  
- Cleaning and summarizing **case study solutions**  
- Building **personal knowledge base** from ChatGPT conversations

---

## 📜 License

MIT License  
Built by [Abhijeet](https://www.linkedin.com/in/abhijeet-099670300/) ⚡

---

## 💬 Future Ideas

- [ ] Web UI (Streamlit-based)
- [ ] API summarization fallback
- [ ] Long context batching (for 100k+ token models)
