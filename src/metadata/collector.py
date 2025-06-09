# metadata/collector.py

import os
from datetime import datetime

def count_lines_and_words(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        lines = f.readlines()
        return len(lines), sum(len(line.split()) for line in lines)

def collect_metadata(base_folder):
    chunk_dir = os.path.join(base_folder, "chunk")
    summary_dir = os.path.join(base_folder, "summarize_chunk")
    log_file = os.path.join(base_folder, "summary_log.txt")

    chunk_files = sorted(f for f in os.listdir(chunk_dir) if f.endswith(".ssf")) if os.path.exists(chunk_dir) else []
    summary_files = sorted(f for f in os.listdir(summary_dir) if f.endswith(".ssf")) if os.path.exists(summary_dir) else []


    # Basic metrics
    total_chunks = len(chunk_files)
    total_summaries = len(summary_files)
    progress_pct = round((total_summaries / total_chunks) * 100, 2) if total_chunks else 0

    # Avg summary time and ETA
    avg_time = None
    eta = None
    last_summary_time = None

    if os.path.exists(log_file):
        timestamps = []
        with open(log_file, "r", encoding="utf-8") as f:
            for line in f:
                if "✅ Done:" in line:
                    time_str = line.split("[")[1].split("]")[0]
                    try:
                        timestamps.append(datetime.strptime(time_str, "%Y-%m-%d %H:%M:%S"))
                    except:
                        pass
        if len(timestamps) >= 2:
            durations = [(t2 - t1).total_seconds() for t1, t2 in zip(timestamps, timestamps[1:])]
            avg_time = sum(durations) / len(durations)
            remaining = total_chunks - total_summaries
            eta = round((remaining * avg_time) / 60, 2)
            last_summary_time = timestamps[-1].isoformat()

    # Word statistics
    chunk_word_lengths = []
    for f in chunk_files:
        fp = os.path.join(chunk_dir, f)
        if os.path.getsize(fp) > 0:
            _, words = count_lines_and_words(fp)
            chunk_word_lengths.append(words)

    summary_word_lengths = []
    for f in summary_files:
        fp = os.path.join(summary_dir, f)
        if os.path.getsize(fp) > 0:
            _, words = count_lines_and_words(fp)
            summary_word_lengths.append(words)

    avg_chunk_words = round(sum(chunk_word_lengths) / len(chunk_word_lengths), 2) if chunk_word_lengths else 0
    avg_summary_words = round(sum(summary_word_lengths) / len(summary_word_lengths), 2) if summary_word_lengths else 0

    return {
        "Total Chunks": total_chunks,
        "Summarized Chunks": total_summaries,
        "Progress %": progress_pct,
        "Average Time per Summary (s)": round(avg_time, 2) if avg_time else "N/A",
        "Estimated Time Left (min)": eta if eta else "N/A",
        "Last Summary Timestamp": last_summary_time if last_summary_time else "N/A",
        "Average Chunk Words": avg_chunk_words,
        "Average Summary Words": avg_summary_words
    }