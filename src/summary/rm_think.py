import os
import re
from utils.log_message import log_message

def remove_think_blocks(base_folder):
    folder_path = os.path.join(base_folder, "summarize_chunk")
    
    # Ensure folder exists
    if not os.path.isdir(folder_path):
        log_message(base_folder, f"❌ Folder not found: {folder_path}")
        return

    # Loop through all matching chunk_summary_X.ssf files
    for filename in os.listdir(folder_path):
        if filename.startswith("chunk_summary_") and filename.endswith(".ssf"):
            file_path = os.path.join(folder_path, filename)

            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()

            # Remove <think>...</think> blocks (non-greedy match)
            cleaned_content = re.sub(r"<think>.*?</think>", "", content, flags=re.DOTALL)

            with open(file_path, "w", encoding="utf-8") as f:
                f.write(cleaned_content)
            
            log_message(base_folder,f"✅ Cleaned: {filename}")

# Example usage:
# remove_think_blocks("your_base_folder_path_here")
