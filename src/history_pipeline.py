import extract_history as eh
import clean_history as ch
import create_chunk as cc

def run_pipeline(base_folder, convo_json_path, lines_per_chunk=5000, overlap_ratio=0.2):
    print("🔍 Step 1: Extracting relevant messages...")
    eh.main(base_folder, convo_json_path)

    print("\n🧹 Step 2: Cleaning extracted messages...")
    ch.clean_project_log(base_folder)

    print("\n📦 Step 3: Splitting cleaned history into overlapping chunks...")
    cc.split_clean_file(base_folder, lines_per_chunk=lines_per_chunk, overlap_ratio=overlap_ratio)

    print("\n✅ Pipeline complete! All files saved in:", base_folder)

if __name__ == "__main__":
    folder = r"speech_to_speech"  # your base folder
    data_path = r"OpenAI April 2025\conversations.json"  # full ChatGPT JSON export
    run_pipeline(folder, data_path, lines_per_chunk=1000, overlap_ratio=0.2)
