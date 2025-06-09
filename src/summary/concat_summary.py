import os, time

from utils.log_message import log_message


def concat_summaries(base_folder: str):
    summary_dir = os.path.join(base_folder, "summarize_chunk")
    output_file = os.path.join(base_folder, "concatenated_summary.ssf")

    if not os.path.exists(summary_dir):
        print(f"❌ base_folder not found: {summary_dir}")
        return

    summary_files = sorted([
        f for f in os.listdir(summary_dir)
        if f.startswith("chunk_summary_") and f.endswith(".ssf")
    ])

    if not summary_files:
        print("⚠️ No summary files found to concatenate.")
        return

    log_message(base_folder, f"🔄 Concatenating {len(summary_files)} summaries...")

    with open(output_file, "w", encoding="utf-8") as outfile:
        for filename in summary_files:
            path = os.path.join(summary_dir, filename)
            with open(path, "r", encoding="utf-8") as infile:
                outfile.write(infile.read().strip())
                outfile.write("\n\n---\n\n")  # separator between chunks

    log_message(base_folder, f"✅ Concatenated summary saved to: {output_file}")

    return 


if __name__ == "__main__":
    base_folder_path = "SIP"
    concat_summaries(base_folder_path)