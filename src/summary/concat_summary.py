import os

def concat_summaries(folder: str):
    summary_dir = os.path.join(folder, "summarize_chunk")
    output_file = os.path.join(folder, "concatenated_summary.ssf")

    if not os.path.exists(summary_dir):
        print(f"❌ Folder not found: {summary_dir}")
        return

    summary_files = sorted([
        f for f in os.listdir(summary_dir)
        if f.startswith("chunk_summary_") and f.endswith(".ssf")
    ])

    if not summary_files:
        print("⚠️ No summary files found to concatenate.")
        return

    print(f"🔄 Concatenating {len(summary_files)} summaries...")

    with open(output_file, "w", encoding="utf-8") as outfile:
        for filename in summary_files:
            path = os.path.join(summary_dir, filename)
            with open(path, "r", encoding="utf-8") as infile:
                outfile.write(infile.read().strip())
                outfile.write("\n\n---\n\n")  # separator between chunks

    print(f"✅ Concatenated summary saved to: {output_file}")


if __name__ == "__main__":
    folder_path = "SIP"
    concat_summaries(folder_path)