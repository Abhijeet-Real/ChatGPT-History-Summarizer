import os

def split_clean_file(base_path, lines_per_chunk=5000, overlap_ratio=0.2):
    """
    Split cleaned history into overlapping chunks.
    Each chunk overlaps the next by a percentage of lines_per_chunk.
    Saves all chunks inside a 'chunk' subfolder within base_path.
    """
    input_path = os.path.join(base_path, "cleaned history.ssf")
    output_dir = os.path.join(base_path, "chunk")
    os.makedirs(output_dir, exist_ok=True)

    with open(input_path, 'r', encoding='utf-8') as f:
        lines = [line.strip() for line in f if line.strip()]  # Remove empty lines

    overlap = int(lines_per_chunk * overlap_ratio)
    step = lines_per_chunk - overlap

    chunk_count = 0
    for i in range(0, len(lines), step):
        chunk = lines[i:i + lines_per_chunk]
        if not chunk:
            break
        chunk_count += 1
        chunk_filename = os.path.join(output_dir, f"chunk_{chunk_count}.ssf")
        with open(chunk_filename, "w", encoding="utf-8") as out_file:
            out_file.write('\n'.join(chunk))

    print(f"✅ Done: Split into {chunk_count} chunks in '{output_dir}'")

if __name__ == "__main__":
    base_folder = r"speech_to_speech"  # ✅ Change to your working folder
    split_clean_file(base_folder, lines_per_chunk=5000, overlap_ratio=0.2)
