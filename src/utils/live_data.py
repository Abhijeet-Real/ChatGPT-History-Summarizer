import os
from datetime import datetime

def count_lines_and_words(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        lines = f.readlines()
        return len(lines), sum(len(line.split()) for line in lines)

def collect_folder_metadata(base_folder):
    metadata = {}

    # --- Chunk Info ---
    chunk_dir = os.path.join(base_folder, "chunk")
    summarize_dir = os.path.join(base_folder, "summarize_chunk")

    chunk_files = sorted(f for f in os.listdir(chunk_dir) if f.endswith(".ssf"))
    summary_files = sorted(f for f in os.listdir(summarize_dir) if f.endswith(".ssf"))

    metadata["chunk_count"] = len(chunk_files)
    metadata["summarized_count"] = len(summary_files)
    metadata["summarized_pct"] = round((len(summary_files) / len(chunk_files)) * 100, 2) if chunk_files else 0

    # --- History Files ---
    for fname in ["extracted history.ssf", "cleaned history.ssf", "keywords.ssf", "summary_log.txt"]:
        path = os.path.join(base_folder, fname)
        if os.path.exists(path):
            lines, words = count_lines_and_words(path)
            size = os.path.getsize(path)
            metadata[f"{fname}_lines"] = lines
            metadata[f"{fname}_words"] = words
            metadata[f"{fname}_size_bytes"] = size
            metadata[f"{fname}_last_modified"] = datetime.fromtimestamp(os.path.getmtime(path)).isoformat()

    return metadata
