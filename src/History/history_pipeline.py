from history import extract_history as eh
from history import clean_history as ch
import os, time

from utils.log_message import log_message



def history_pipeline(base_folder, convo_json_path):
    log_message(base_folder, "🔍 Step 1: Extracting relevant messages...")
    eh.main(base_folder, convo_json_path)

    log_message(base_folder, "🧹 Step 2: Cleaning extracted messages...")
    ch.clean_project_log(base_folder)

if __name__ == "__main__":
    folder = r"SIP"  # your base folder
    data_path = r"OpenAI June 2025\conversations.json"  # full ChatGPT JSON export
    history_pipeline(folder, data_path, lines_per_chunk=1000, overlap_ratio=0.2)
